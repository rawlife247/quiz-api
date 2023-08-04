from datetime import timedelta

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Category, Tag, Quiz, Question, Answer, Participant, Feedback
from django.utils import timezone

from .tasks import schedule_report_generation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def validate_name(self, value):
        exists_already = Category.objects.filter(name__iexact=value).exists()
        if exists_already:
            raise serializers.ValidationError('Category with this name is already exist')
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

    def validate_name(self, value):
        exists_already = Tag.objects.filter(name__iexact=value).exists()
        if exists_already:
            raise serializers.ValidationError('Tag with this name is already exist')
        return value


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'is_correct',)

    def create(self, validated_data):
        question_id = self.context['view'].kwargs['pk']
        question = Question.objects.filter(pk=question_id).exists()
        if not question:
            raise serializers.ValidationError({'error': 'Invalid question ID'})

        answer = Answer.objects.create(question_id=question_id, **validated_data)

        return answer


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'points', 'answers')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', None)
        quiz_id = self.context['view'].kwargs['pk']
        quiz = Quiz.objects.filter(pk=quiz_id).exists()
        if not quiz:
            raise serializers.ValidationError({'error': 'Invalid quiz ID'})

        question = Question.objects.create(quiz_id=quiz_id, **validated_data)
        if answers_data is not None:
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.type = validated_data.get('type', instance.type)
        instance.points = validated_data.get('points', instance.points)
        instance.save()

        return instance


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False, write_only=True)
    questions_link = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Quiz
        fields = (
            'id', 'title', 'description', 'time_limit', 'passing_marks_percentage', 'tags', 'categories', 'created_by',
            'questions', 'questions_link')
        read_only_fields = ['created_by', ]

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', None)
        tags = validated_data.pop('tags')
        categories = validated_data.pop('categories')

        quiz = Quiz.objects.create(**validated_data)
        quiz.tags.set(tags)
        quiz.categories.set(categories)

        if questions_data is not None:
            for question_data in questions_data:
                answers_data = question_data.pop('answers')
                question = Question.objects.create(quiz=quiz, **question_data)

                for answer_data in answers_data:
                    Answer.objects.create(question=question, **answer_data)

        return quiz

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.time_limit = validated_data.get('time_limit', instance.time_limit)

        tags_data = validated_data.get('tags', instance.tags)
        instance.tags.set(tags_data)

        categories_data = validated_data.get('categories', instance.categories)
        instance.categories.set(categories_data)

        instance.save()

        return instance

    def validate_time_limit(self, attrs):
        if attrs['time_limit'] < 1:
            raise serializers.ValidationError('Time limit should be more than 1 minute')
        if attrs['time_limit'] > 240:
            raise serializers.ValidationError('Time limit should be less than 240 minutes (4 hours)')
        return attrs

    def get_questions_link(self, obj):
        return reverse('quiz:question-list-create', args=[obj.pk], request=self.context.get('request'))


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer = serializers.IntegerField()

    def validate(self, data):
        question_id = data.get('question_id')
        selected_answer = data.get('selected_answer')

        try:
            question = Question.objects.get(id=question_id)
            Answer.objects.get(id=selected_answer, question=question)
        except Question.DoesNotExist:
            raise serializers.ValidationError("Invalid question ID")
        except Answer.DoesNotExist:
            raise serializers.ValidationError("Invalid selected answer / answer is not belong to the given question")

        return data


class SubmitQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = SubmitAnswerSerializer(many=True)
    score = serializers.IntegerField(read_only=True)

    def calculate_score(self, quiz, answers):
        score = 0
        for answer_data in answers:
            serializer = SubmitAnswerSerializer(data=answer_data)
            serializer.is_valid(raise_exception=True)

            question_id = serializer.validated_data['question_id']
            selected_answer = serializer.validated_data['selected_answer']
            try:
                question = Question.objects.get(id=question_id, quiz=quiz)
            except Question.DoesNotExist:
                raise serializers.ValidationError("question is not belong to the given Quiz")

            correct_answers = Answer.objects.filter(question=question, is_correct=True)
            if correct_answers.filter(id=selected_answer).exists():
                score += question.points

        return score

    def validate(self, data):
        quiz_id = data.get('quiz_id')
        answers = data.get('answers')

        try:
            quiz = Quiz.objects.get(id=quiz_id)
            participant = Participant.objects.get(user=self.context['request'].user, quiz=quiz)

            tolerance_window = timedelta(seconds=30)
            current_time = timezone.now()
            if current_time > participant.end_time + tolerance_window:
                raise serializers.ValidationError("Participant's time is over. Submission not allowed.")

        except Quiz.DoesNotExist:
            raise serializers.ValidationError("Invalid quiz ID")
        except Participant.DoesNotExist:
            raise serializers.ValidationError("Participant not found")

        score = self.calculate_score(quiz, answers)
        data['score'] = score

        return data

    def save(self):
        user = self.context['request'].user
        quiz_id = self.validated_data['quiz_id']
        score = self.validated_data['score']
        quiz = Quiz.objects.get(id=quiz_id)

        participant = Participant.objects.get(user=user, quiz=quiz)
        participant.score = score

        if quiz.passing_marks_percentage > 0:
            passing_marks = quiz.get_total_points() * (quiz.passing_marks_percentage / 100)
            participant.has_passed = score >= passing_marks

        participant.save()

        schedule_report_generation(participant.id)


class FeedbackSerializer(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ('id', 'rating', 'comment', 'participant')

    def get_participant(self, obj):
        return obj.participant.user.username

    def validate(self, data):
        quiz_id = self.context['view'].kwargs['pk']
        user = self.context['user']

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid quiz ID'})

        try:
            participant = Participant.objects.get(quiz=quiz, user=user)
        except Participant.DoesNotExist:
            raise serializers.ValidationError("You can provide feedback after taking the quiz")

        data['quiz'] = quiz
        data['participant'] = participant
        return data

    def create(self, validated_data):
        return Feedback.objects.create(**validated_data)


class ParticipantSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    quiz_id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ('quiz_id', 'quiz', 'user', 'score', 'start_time')

    def get_quiz_id(self, obj):
        return obj.quiz.id

    def get_quiz(self, obj):
        return obj.quiz.title

    def get_user(self, obj):
        return obj.user.username


class UserQuizStatisticsSerializer(serializers.ModelSerializer):
    quiz_id = serializers.ReadOnlyField(source='quiz.id')
    quiz_title = serializers.ReadOnlyField(source='quiz.title')
    quiz_total_marks = serializers.SerializerMethodField()
    has_passed = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = [
            'quiz_id',
            'quiz_title',
            'quiz_total_marks',
            'score',
            'date',
            'has_passed',
        ]

    def get_quiz_total_marks(self, participant):
        return participant.quiz.get_total_points()

    def get_has_passed(self, participant):
        return participant.has_passed

    def get_date(self, participant):
        return participant.start_time

from rest_framework import serializers
from .models import Category, Tag, Quiz, Question, Answer, Participant, Feedback
from django.utils import timezone


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
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'time_limit', 'tags', 'categories', 'created_by', 'questions')
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

            current_time = timezone.now()
            if current_time > participant.end_time:
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
        participant.save()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'rating', 'comment')

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

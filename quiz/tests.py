from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Tag, Quiz, Question, Answer, Participant, Feedback
from .serializers import (
    CategorySerializer, TagSerializer, QuizSerializer
)
from account.models import UserProfile
from django.utils import timezone
from datetime import timedelta


class CategoryListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        url = reverse('quiz:category-list-create')
        data = {'name': 'Test Category'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.get().name, 'Test Category')

    def test_list_categories(self):
        url = reverse('quiz:category-list-create')
        Category.objects.create(name='Category 1')
        Category.objects.create(name='Category 2')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        serializer_data = CategorySerializer(Category.objects.all(), many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(Category.objects.count(), 2)


class CategoryRetrieveUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='user', is_staff=True)
        self.category = Category.objects.create(name='Test Category')
        self.url = reverse('quiz:category-retrieve-update-delete', args=[self.category.id])
        self.client.force_authenticate(user=self.user)

    def test_retrieve_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category(self):
        new_name = 'New Category Name'
        response = self.client.put(self.url, {'name': new_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, new_name)

    def test_delete_category(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class TagListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_create_tag(self):
        url = reverse('quiz:tag-list-create')
        data = {'name': 'Test Tag'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.get().name, 'Test Tag')

    def test_list_tag(self):
        url = reverse('quiz:tag-list-create')
        Tag.objects.create(name='Tag 1')
        Tag.objects.create(name='Tag 2')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        serializer_data = TagSerializer(Tag.objects.all(), many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(Tag.objects.count(), 2)


class TagRetrieveUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='user', is_staff=True)
        self.tag = Tag.objects.create(name='Test tag')
        self.url = reverse('quiz:tag-retrieve-update-delete', args=[self.tag.id])
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tag(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.tag.id)
        self.assertEqual(response.data['name'], self.tag.name)

    def test_update_tag(self):
        new_name = 'New tag Name'
        response = self.client.put(self.url, {'name': new_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, new_name)

    def test_delete_tag(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())


class QuizListCreateViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('quiz:quiz-list-create')
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.tag = Tag.objects.create(name='Test tag')
        self.category = Category.objects.create(name='Test category')

    def test_create_quiz(self):
        data = {
            "title": "Test Quiz",
            "description": "Test Description",
            "time_limit": 30,
            "tags": [self.tag.id],
            "categories": [self.category.id],
            "questions": [
                {
                    "text": "Test question",
                    "type": "MC",
                    "points": 3,
                    "answers": [
                        {
                            "text": "testing answer 1",
                            "is_correct": True
                        },
                        {
                            "text": "testing answer 2",
                            "is_correct": False
                        },
                        {
                            "text": "testing answer 3",
                            "is_correct": False
                        }
                    ]
                }
            ]
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)

        quiz = Quiz.objects.get()

        self.assertEqual(quiz.title, 'Test Quiz')
        self.assertEqual(quiz.description, 'Test Description')
        self.assertEqual(quiz.time_limit, 30)

        self.assertTrue(quiz.tags.filter(id=self.tag.id).exists())
        self.assertTrue(quiz.categories.filter(id=self.category.id).exists())

        self.assertEqual(quiz.questions.count(), 1)
        self.assertTrue(quiz.questions.filter(text__exact='Test question'))
        self.assertEqual(quiz.questions.filter(text__exact='Test question').first().answers.count(), 3)

        self.assertEqual(quiz.created_by, self.user)

    def test_list_quizzes(self):
        Quiz.objects.create(title='Quiz 1', created_by=self.user, time_limit=30)
        Quiz.objects.create(title='Quiz 2', created_by=self.user, time_limit=45)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        serializer_data = QuizSerializer(Quiz.objects.all(), many=True).data
        self.assertEqual(response.data, serializer_data)


class QuizRetrieveUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.tag = Tag.objects.create(name='Test tag')
        self.category = Category.objects.create(name='Test category')

        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test Description',
            time_limit=30,
            created_by=self.user
        )
        self.quiz.tags.add(self.tag)
        self.quiz.categories.add(self.category)

        self.question = Question.objects.create(
            quiz=self.quiz,
            text='Test question',
            type='MC',
            points=3
        )
        self.answer1 = Answer.objects.create(
            question=self.question,
            text='testing answer 1',
            is_correct=True
        )
        self.answer2 = Answer.objects.create(
            question=self.question,
            text='testing answer 2',
            is_correct=False
        )
        self.answer3 = Answer.objects.create(
            question=self.question,
            text='testing answer 3',
            is_correct=False
        )

        self.url = reverse('quiz:quiz-retrieve-update-delete', kwargs={'pk': self.quiz.pk})

    def test_retrieve_quiz(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.quiz.id)
        self.assertEqual(response.data['title'], self.quiz.title)
        self.assertEqual(response.data['description'], self.quiz.description)
        self.assertEqual(response.data['time_limit'], self.quiz.time_limit)
        self.assertEqual(response.data['created_by'], self.quiz.created_by_id)

        self.assertIn('tags', response.data)
        self.assertIn('categories', response.data)

        self.assertIn('questions', response.data)
        questions_data = response.data['questions']

        self.assertEqual(len(questions_data), 1)
        question_data = questions_data[0]

        self.assertEqual(question_data['text'], self.question.text)
        self.assertEqual(question_data['type'], self.question.type)
        self.assertEqual(question_data['points'], self.question.points)
        self.assertIn('answers', question_data)
        answers_data = question_data['answers']
        self.assertEqual(len(answers_data), 3)

    def test_update_quiz(self):
        updated_data = {
            'title': 'Updated Quiz',
            'description': 'Updated Description',
            'time_limit': 45,
            'tags': [1],
            'categories': [1]
        }

        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, 'Updated Quiz')
        self.assertEqual(self.quiz.description, 'Updated Description')
        self.assertEqual(self.quiz.time_limit, 45)

        self.assertTrue(self.quiz.tags.filter(id=1).exists())
        self.assertTrue(self.quiz.categories.filter(id=1).exists())

    def test_delete_quiz(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Quiz.objects.filter(pk=self.quiz.pk).exists())
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())
        self.assertFalse(Answer.objects.filter(pk=self.answer1.pk).exists())
        self.assertFalse(Answer.objects.filter(pk=self.answer2.pk).exists())
        self.assertFalse(Answer.objects.filter(pk=self.answer3.pk).exists())


class StartQuizViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('quiz:start-quiz')
        self.user = UserProfile.objects.create(username='admin')
        self.client.force_authenticate(user=self.user)
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', time_limit=30,
                                        created_by=self.user)

    def test_start_quiz(self):
        data = {'quiz_id': self.quiz.id}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        participant = Participant.objects.get(user=self.user, quiz=self.quiz)
        self.assertIsNotNone(participant.start_time)
        self.assertIsNotNone(participant.end_time)
        self.assertIsNone(participant.score)

    def test_start_quiz_invalid_quiz_id(self):
        data = {'quiz_id': 999}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubmitQuizViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('quiz:submit-quiz')
        self.user = UserProfile.objects.create(username='admin')
        self.client.force_authenticate(user=self.user)

        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', time_limit=30,
                                        created_by=self.user)
        self.participant = Participant.objects.create(user=self.user, quiz=self.quiz, start_time=timezone.now(),
                                                      end_time=timezone.now() + timedelta(minutes=self.quiz.time_limit))
        self.question1 = Question.objects.create(quiz=self.quiz, text='Test question 1', type='MC', points=3)
        self.answer1 = Answer.objects.create(question=self.question1, text='Answer 1', is_correct=False)
        self.answer2 = Answer.objects.create(question=self.question1, text='Answer 2', is_correct=True)

        self.question2 = Question.objects.create(quiz=self.quiz, text='Test question 2', type='MC', points=5)
        self.answer3 = Answer.objects.create(question=self.question2, text='Answer 3', is_correct=True)
        self.answer4 = Answer.objects.create(question=self.question2, text='Answer 4', is_correct=False)

        self.question3 = Question.objects.create(quiz=self.quiz, text='Test question 3', type='MC', points=8)
        self.answer5 = Answer.objects.create(question=self.question3, text='Answer 5', is_correct=True)
        self.answer6 = Answer.objects.create(question=self.question3, text='Answer 6', is_correct=False)

    def test_submit_quiz(self):
        data = {
            'quiz_id': self.quiz.id,
            'answers': [
                {
                    'question_id': self.question1.id,
                    'selected_answer': self.answer2.id
                },
                {
                    'question_id': self.question2.id,
                    'selected_answer': self.answer4.id
                },
                {
                    'question_id': self.question3.id,
                    'selected_answer': self.answer5.id
                },

            ]
        }

        response = self.client.post(self.url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.participant.refresh_from_db()
        self.assertIsNotNone(self.participant.score)
        self.assertEqual(self.participant.score, 11)

    def test_submit_quiz_invalid_quiz_id(self):
        data = {'quiz_id': 999, 'answers': []}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class QuestionListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', time_limit=20,
                                        created_by=self.user)
        self.url = reverse('quiz:question-list-create', kwargs={'pk': self.quiz.pk})

    def test_create_question(self):
        data = {
            'text': 'Test question',
            'type': 'MC',
            'points': 3,
            'answers': [
                {
                    'text': 'Answer 1',
                    'is_correct': True
                },
                {
                    'text': 'Answer 2',
                    'is_correct': False
                }
            ]
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        question = Question.objects.get()

        self.assertEqual(question.text, 'Test question')
        self.assertEqual(question.type, 'MC')
        self.assertEqual(question.points, 3)

        answers = question.answers.all()
        self.assertEqual(answers.count(), 2)

        answer1 = answers[0]
        self.assertEqual(answer1.text, 'Answer 1')
        self.assertEqual(answer1.is_correct, True)

        answer2 = answers[1]
        self.assertEqual(answer2.text, 'Answer 2')
        self.assertEqual(answer2.is_correct, False)

    def test_get_question_list(self):
        Question.objects.create(quiz=self.quiz, text='Question 1', type='MC', points=2)
        Question.objects.create(quiz=self.quiz, text='Question 2', type='OE', points=1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)

        question1 = data[0]

        self.assertEqual(question1['text'], 'Question 1')
        self.assertEqual(question1['type'], 'MC')
        self.assertEqual(question1['points'], 2)

        question2 = data[1]

        self.assertEqual(question2['text'], 'Question 2')
        self.assertEqual(question2['type'], 'OE')
        self.assertEqual(question2['points'], 1)


class QuestionRetrieveUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', time_limit=20,
                                        created_by=self.user)
        self.question = Question.objects.create(quiz=self.quiz, text='Test question', type='MC', points=3)
        self.url = reverse('quiz:question-retrieve-update-delete', kwargs={'pk': self.question.pk})

    def test_get_question(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data['text'], 'Test question')
        self.assertEqual(data['type'], 'MC')
        self.assertEqual(data['points'], 3)

    def test_update_question(self):
        data = {
            'text': 'Updated question',
            'type': 'OE',
            'points': 2
        }

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.question.refresh_from_db()
        self.assertEqual(self.question.text, 'Updated question')
        self.assertEqual(self.question.type, 'OE')
        self.assertEqual(self.question.points, 2)

    def test_delete_question(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())


class AnswerListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.quiz = Quiz.objects.create(
            time_limit=30,
            created_by=self.user
        )
        self.question = Question.objects.create(text='Test question', quiz=self.quiz)
        self.url = reverse('quiz:answer-list-create', kwargs={'pk': self.question.pk})

    def test_create_answer(self):
        data = {
            'text': 'Test answer',
            'is_correct': True
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        answer = Answer.objects.get()
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.text, 'Test answer')
        self.assertEqual(answer.is_correct, True)

    def test_get_answer_list(self):
        Answer.objects.create(question=self.question, text='Answer 1', is_correct=False)
        Answer.objects.create(question=self.question, text='Answer 2', is_correct=True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)

        answer1 = data[0]

        self.assertEqual(answer1['text'], 'Answer 1')
        self.assertEqual(answer1['is_correct'], False)

        answer2 = data[1]

        self.assertEqual(answer2['text'], 'Answer 2')
        self.assertEqual(answer2['is_correct'], True)


class AnswerRetrieveUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin', is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.quiz = Quiz.objects.create(
            time_limit=30,
            created_by=self.user
        )
        self.question = Question.objects.create(text='Test question', quiz=self.quiz)
        self.answer = Answer.objects.create(question=self.question, text='Test answer', is_correct=True)
        self.url = reverse('quiz:answer-retrieve-update-delete', kwargs={'pk': self.answer.pk})

    def test_get_answer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data['text'], 'Test answer')
        self.assertEqual(data['is_correct'], True)

    def test_update_answer(self):
        data = {
            'text': 'Updated answer',
            'is_correct': False
        }

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.answer.refresh_from_db()
        self.assertEqual(self.answer.text, 'Updated answer')
        self.assertEqual(self.answer.is_correct, False)

    def test_delete_answer(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Answer.objects.filter(pk=self.answer.pk).exists())


class FeedbackListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin')
        self.client.force_authenticate(user=self.user)
        self.quiz = Quiz.objects.create(title='Test Quiz', time_limit=50, created_by=self.user)
        self.url = reverse('quiz:feedback-list-create', kwargs={'pk': self.quiz.pk})
        self.participant = Participant.objects.create(user=self.user, quiz=self.quiz, start_time=timezone.now(),
                                                      end_time=timezone.now())

    def test_create_feedback(self):
        data = {
            'rating': 5,
            'comment': 'Great quiz!'
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        feedback = Feedback.objects.get()
        self.assertEqual(feedback.quiz, self.quiz)
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.comment, 'Great quiz!')

    def test_get_feedback_list(self):
        Feedback.objects.create(quiz=self.quiz, rating=4, comment='Good quiz', participant=self.participant)
        Feedback.objects.create(quiz=self.quiz, rating=3, comment='Average quiz', participant=self.participant)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 2)

        feedback1 = data[0]
        self.assertEqual(feedback1['rating'], 4)
        self.assertEqual(feedback1['comment'], 'Good quiz')

        feedback2 = data[1]
        self.assertEqual(feedback2['rating'], 3)
        self.assertEqual(feedback2['comment'], 'Average quiz')


class FeedbackRetrieveUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username='admin')
        self.client.force_authenticate(user=self.user)

        self.quiz = Quiz.objects.create(title='Test Quiz', time_limit=50, created_by=self.user)
        self.participant = Participant.objects.create(user=self.user, quiz=self.quiz, start_time=timezone.now(),
                                                      end_time=timezone.now())
        self.feedback = Feedback.objects.create(quiz=self.quiz, rating=4, comment='Good quiz',
                                                participant=self.participant)
        self.url = reverse('quiz:feedback-retrieve-update-delete', kwargs={'pk': self.feedback.pk})

    def test_get_feedback(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['rating'], 4)
        self.assertEqual(data['comment'], 'Good quiz')

    def test_update_feedback(self):
        data = {
            'rating': 3,
            'comment': 'Average quiz'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.feedback.refresh_from_db()
        self.assertEqual(self.feedback.rating, 3)
        self.assertEqual(self.feedback.comment, 'Average quiz')

    def test_delete_feedback(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Feedback.objects.filter(pk=self.feedback.pk).exists())

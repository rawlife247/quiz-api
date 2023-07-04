from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from datetime import timedelta

from .models import Category, Tag, Quiz, Question, Answer, Participant, Feedback
from .serializers import (
    CategorySerializer, TagSerializer, QuizSerializer,
    QuestionSerializer, AnswerSerializer, FeedbackSerializer, SubmitQuizSerializer
)
from .permissions import IsStaffOrReadOnly, IsAuthenticatedOrReadOnly, IsFeedbackOwner

from django.utils.decorators import method_decorator

from .swagger import *


@method_decorator(name='get', decorator=category_list_swagger_schema())
@method_decorator(name='post', decorator=category_create_swagger_schema())
class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsStaffOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(name='get', decorator=category_retrieve_swagger_schema())
@method_decorator(name='put', decorator=category_update_swagger_schema())
@method_decorator(name='delete', decorator=category_delete_swagger_schema())
class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)


@method_decorator(name='get', decorator=tag_list_swagger_schema())
@method_decorator(name='post', decorator=tag_create_swagger_schema())
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsStaffOrReadOnly,)


@method_decorator(name='get', decorator=tag_retrieve_swagger_schema())
@method_decorator(name='put', decorator=tag_update_swagger_schema())
@method_decorator(name='delete', decorator=tag_delete_swagger_schema())
class TagRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsStaffOrReadOnly,)


@method_decorator(name='get', decorator=quiz_list_swagger_schema())
@method_decorator(name='post', decorator=quiz_create_swagger_schema())
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    permission_classes = (IsStaffOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@method_decorator(name='get', decorator=quiz_retrieve_swagger_schema())
@method_decorator(name='put', decorator=quiz_update_swagger_schema())
@method_decorator(name='delete', decorator=quiz_delete_swagger_schema())
class QuizRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsStaffOrReadOnly,)


@method_decorator(name='post', decorator=start_quiz_swagger_schema())
class StartQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get('quiz_id')

        try:
            quiz = Quiz.objects.get(id=quiz_id)

        except Quiz.DoesNotExist:
            return Response({'quiz_id': 'Invalid quiz ID'}, status=status.HTTP_400_BAD_REQUEST)

        start_time = timezone.now()
        time_limit = quiz.time_limit
        end_time = start_time + timedelta(minutes=time_limit)

        try:
            participant = Participant.objects.get(user=user, quiz=quiz)
            participant.start_time = start_time
            participant.end_time = end_time
            participant.score = None
            participant.save()

        except Participant.DoesNotExist:
            Participant.objects.create(user=user, quiz=quiz, start_time=start_time, end_time=end_time, score=None)

        return Response({'message': 'Quiz started successfully'}, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=submit_quiz_swagger_schema())
class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SubmitQuizSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Quiz submitted successfully', 'data': serializer.data})


@method_decorator(name='get', decorator=question_list_swagger_schema())
@method_decorator(name='post', decorator=question_create_swagger_schema())
class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsStaffOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Question.objects.filter(quiz_id=pk)


@method_decorator(name='get', decorator=question_retrieve_swagger_schema())
@method_decorator(name='put', decorator=question_update_swagger_schema())
@method_decorator(name='delete', decorator=question_delete_swagger_schema())
class QuestionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsStaffOrReadOnly,)


@method_decorator(name='get', decorator=answer_list_swagger_schema())
@method_decorator(name='post', decorator=answer_create_swagger_schema())
class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsStaffOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Answer.objects.filter(question_id=pk)


@method_decorator(name='get', decorator=answer_retrieve_swagger_schema())
@method_decorator(name='put', decorator=answer_update_swagger_schema())
@method_decorator(name='delete', decorator=answer_delete_swagger_schema())
class AnswerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsStaffOrReadOnly,)


@method_decorator(name='get', decorator=feedback_list_swagger_schema())
@method_decorator(name='post', decorator=feedback_create_swagger_schema())
class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Feedback.objects.filter(quiz_id=pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


@method_decorator(name='get', decorator=feedback_retrieve_swagger_schema())
@method_decorator(name='put', decorator=feedback_update_swagger_schema())
@method_decorator(name='delete', decorator=feedback_delete_swagger_schema())
class FeedbackRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsFeedbackOwner,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

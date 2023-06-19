from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from datetime import timedelta

from .models import Category, Tag, Quiz, Question, Answer, Participant, Feedback
from .serializers import (
    CategorySerializer, TagSerializer, QuizSerializer,
    QuestionSerializer, AnswerSerializer, FeedbackSerializer, SubmitQuizSerializer
)
from .permissions import IsStaffOrReadOnly, IsAuthenticatedOrReadOnly, UpdateOwnFeedback


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class TagRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuizRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class StartQuizView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

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





class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = SubmitQuizSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Quiz submitted successfully', 'data': serializer.data})


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Question.objects.filter(quiz_id=pk)


class QuestionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Answer.objects.filter(question_id=pk)


class AnswerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsStaffOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Feedback.objects.filter(quiz_id=pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class FeedbackRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (UpdateOwnFeedback,)
    authentication_classes = (TokenAuthentication,)



# class SubmitQuizView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (TokenAuthentication,)
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         quiz_id = request.data.get('quiz_id')
#         answers = request.data.get('answers')
#
#         if answers is None:
#             return Response({'answers': 'Answers not provided'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             quiz = Quiz.objects.get(id=quiz_id)
#             participant = Participant.objects.get(user=user, quiz=quiz)
#         except Quiz.DoesNotExist:
#             return Response({'quiz_id': 'Invalid quiz ID'}, status=status.HTTP_400_BAD_REQUEST)
#         except Participant.DoesNotExist:
#             return Response({'user': 'Participant not found'}, status=status.HTTP_400_BAD_REQUEST)
#
#         score = 0
#
#         for answer_data in answers:
#             serializer = AnswerSubmissionSerializer(data=answer_data)
#             if serializer.is_valid():
#                 question_id = serializer.validated_data['question_id']
#                 selected_answer = serializer.validated_data['selected_answer']
#
#                 try:
#                     question = Question.objects.get(id=question_id, quiz=quiz)
#                     correct_answers = Answer.objects.filter(question=question, is_correct=True)
#
#                     if correct_answers.filter(id=selected_answer).exists():
#                         score += question.point
#                 except Question.DoesNotExist:
#                     return Response({'question_id': 'Invalid question ID or it does not belong to the given Quiz'},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         participant.score = score
#         participant.save()
#
#         return Response({'message': 'Quiz submitted successfully', 'score': score})
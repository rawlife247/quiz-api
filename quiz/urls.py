from django.urls import path
from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDeleteView,
    TagListCreateView, TagRetrieveUpdateDeleteView,
    QuizListCreateView, QuizRetrieveUpdateDeleteView,
    QuestionListCreateView, QuestionRetrieveUpdateDeleteView,
    AnswerListCreateView, AnswerRetrieveUpdateDeleteView,
    FeedbackListCreateView, FeedbackRetrieveUpdateDeleteView, SubmitQuizView, StartQuizView
)

app_name = 'quiz'

urlpatterns = [
    path('quizzes/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('quizzes/categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(),
         name='category-retrieve-update-delete'),

    path('quizzes/tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('quizzes/tags/<int:pk>/', TagRetrieveUpdateDeleteView.as_view(), name='tag-retrieve-update-delete'),

    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDeleteView.as_view(), name='quiz-retrieve-update-delete'),
    path('quizzes/<int:pk>/questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('quizzes/start/', StartQuizView.as_view(), name='start-quiz'),
    path('quizzes/submit/', SubmitQuizView.as_view(), name='submit-quiz'),

    path('questions/<int:pk>/', QuestionRetrieveUpdateDeleteView.as_view(), name='question-retrieve-update-delete'),
    path('questions/<int:pk>/answers/', AnswerListCreateView.as_view(), name='answer-list-create'),

    path('answers/<int:pk>/', AnswerRetrieveUpdateDeleteView.as_view(), name='answer-retrieve-update-delete'),

    path('quizzes/<int:pk>/feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackRetrieveUpdateDeleteView.as_view(), name='feedback-retrieve-update-delete')
]

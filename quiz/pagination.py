from rest_framework.pagination import PageNumberPagination


class QuestionsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'qs'
    max_page_size = 20


class QuizzesSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'quizzes'
    max_page_size = 15


class FeedbackSetPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'feedbacks'
    max_page_size = 15


class LeaderboardPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'participants'
    max_page_size = 50

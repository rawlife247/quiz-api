from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'account'

router = DefaultRouter()
router.register('users', views.UserViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot-password-confirm/<str:token>/', views.ForgotPasswordConfirmView.as_view(), name='forgot-password')

]

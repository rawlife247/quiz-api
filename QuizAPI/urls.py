from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls', namespace='account')),
    path('api/', include('quiz.urls', namespace='quiz')),

]

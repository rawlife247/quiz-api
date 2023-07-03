from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version='v1',
        contact=openapi.Contact(email="rayhanbillah@hotmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

docs_url = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls', namespace='account')),
    path('api/', include('quiz.urls', namespace='quiz')),

]
urlpatterns = urlpatterns + docs_url

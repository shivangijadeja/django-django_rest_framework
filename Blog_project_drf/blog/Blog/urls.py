from django.urls import path,include
from .views import CategoryApi,BlogApi
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('category/',CategoryApi.as_view()),
    path('blog/',BlogApi.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
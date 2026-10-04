from django.urls import path
from . import views

urlpatterns = [
    path('check-update/', views.check_update, name='check-update'),
    path('upload-version/', views.upload_version_api, name='upload_version_api'),
]

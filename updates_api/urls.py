from django.urls import path
from . import views

urlpatterns = [
    path('check-update/', views.check_update, name='check-update'),
]

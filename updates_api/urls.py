from django.urls import path
from . import views

urlpatterns = [
    path('check-update/', views.check_update, name='check-update'),
    path('dashboard/', views.custom_admin_dashboard, name='custom_admin'),
    path('dashboard/delete/<int:pk>/', views.delete_version, name='delete_version'),
]

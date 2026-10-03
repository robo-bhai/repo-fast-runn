from django.urls import path
from . import views

urlpatterns = [
    # Public Hadi88 App Store Home page
    path('', views.app_store_home, name='app_store_home'),
    
    # Existing Android App Update API endpoint
    path('check-update/', views.check_update, name='check-update'),
]

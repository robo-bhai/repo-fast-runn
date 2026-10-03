"""
URL configuration for batvoice_server project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # App Store home page direct root par (hadi88.online/)
    path('', include('updates_api.urls')),
    
    # Agar aap purani /api/ check-update bhi sath chalana chahte hain toh ye rakhein:
    # path('api/', include('updates_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

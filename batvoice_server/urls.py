"""
URL configuration for batvoice_server project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin panel sirf /admin/ par
    path('admin/', admin.site.urls),
    
    # 2. App Store home page direct root par (e.g., https://update-bat.uqn88.store/)
    path('', include('updates_api.urls')),
    
    # 3. Agar mobile app purani /api/ check-update URL use kar rahi hai toh yeh bhi sath active rahega
    path('api/', include('updates_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

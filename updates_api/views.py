from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .models import AppVersion

@require_GET
def check_update(request):
    """
    API Endpoint called by BatVoice Android app:
    GET /api/check-update/
    """
    latest_version = AppVersion.objects.filter(is_active=True).order_by('-version_code').first()

    if not latest_version:
        return JsonResponse({
            'status': 'no_version_available',
            'latest_version_code': 0,
            'latest_version_name': '0.0.0',
            'release_notes': 'No active release available.',
            'apk_download_url': '',
            'force_update': False,
            'file_size_mb': 0.0
        })

    apk_url = ''
    if latest_version.apk_file:
        apk_url = request.build_absolute_uri(latest_version.apk_file.url)

    return JsonResponse({
        'status': 'success',
        'latest_version_code': latest_version.version_code,
        'latest_version_name': latest_version.version_name,
        'release_notes': latest_version.release_notes,
        'apk_download_url': apk_url,
        'force_update': latest_version.force_update,
        'file_size_mb': latest_version.file_size_mb
    })


@require_GET
def app_store_home(request):
    """
    Public App Store View for Hadi88 domain:
    GET /
    """
    # Sirf active versions fetch honge aur latest pehle show hoga
    apps = AppVersion.objects.filter(is_active=True).order_by('-version_code')
    return render(request, 'store/index.html', {'apps': apps})

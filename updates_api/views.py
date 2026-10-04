import os
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
@require_POST
def upload_version_api(request):
    """
    API Endpoint called by GitHub Actions:
    POST /api/upload-version/
    """
    # 1. Security Check (Token verification from headers)
    auth_header = request.headers.get('Authorization', '')
    expected_token = os.environ.get('DJANGO_API_KEY', '6554330545hgshdjgsqqh') # Aap env variable ya hardcoded key rakh sakte hain
    
    # Agar aapne server par environment variable set kiya hai, toh us se match karein
    if auth_header != f"Bearer {expected_token}":
        return JsonResponse({'status': 'error', 'message': 'Unauthorized request!'}, status=401)

    try:
        # 2. Form data se values nikalna
        version_code = request.POST.get('version_code')
        version_name = request.POST.get('version_name')
        file_size_mb = request.POST.get('file_size_mb', 0.0)
        release_notes = request.POST.get('release_notes', 'Automatic release built via GitHub Actions.')
        apk_file = request.FILES.get('apk_file')

        if not version_code or not version_name or not apk_file:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields (version_code, version_name, or apk_file).'}, status=400)

        # Optional: Purane versions ko inactive karna ho ya naye ko active rakhna ho
        # Pehle sabhi ko active se hata sakte hain agar sirf ek hi latest active rakhna ho:
        AppVersion.objects.filter(is_active=True).update(is_active=False)

        # 3. Naya version database mein save karna
        new_version = AppVersion.objects.create(
            version_code=int(version_code),
            version_name=version_name,
            file_size_mb=float(file_size_mb),
            release_notes=release_notes,
            apk_file=apk_file,
            is_active=True,
            force_update=False # Aap chahein toh ise bhi POST data se control kar sakte hain
        )

        return JsonResponse({
            'status': 'success',
            'message': 'APK and version uploaded successfully!',
            'version_code': new_version.version_code,
            'version_name': new_version.version_name
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

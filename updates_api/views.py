from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
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


@login_required(login_url='/admin/login/')
def custom_admin_dashboard(request):
    """
    Custom Admin Dashboard View to manage versions and upload new APKs directly.
    """
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            version_code = request.POST.get('version_code')
            version_name = request.POST.get('version_name')
            release_notes = request.POST.get('release_notes')
            force_update = True if request.POST.get('force_update') == 'on' else False
            is_active = True if request.POST.get('is_active') == 'on' else False
            apk_file = request.FILES.get('apk_file')

            if not version_code or not version_name or not apk_file:
                raise ValueError("Version Code, Version Name, and APK File are required fields.")

            # Create new AppVersion entry
            AppVersion.objects.create(
                version_code=int(version_code),
                version_name=version_name,
                release_notes=release_notes,
                force_update=force_update,
                is_active=is_active,
                apk_file=apk_file
            )
            success_message = "New APK version uploaded successfully!"
            return redirect('custom_admin')
        except Exception as e:
            error_message = str(e)

    total_versions = AppVersion.objects.count()
    active_versions_count = AppVersion.objects.filter(is_active=True).count()
    versions = AppVersion.objects.all()[:10] # Recent 10 versions

    context = {
        'total_versions': total_versions,
        'active_versions_count': active_versions_count,
        'versions': versions,
        'error_message': error_message,
        'success_message': success_message,
    }
    return render(request, 'store/admin_dashboard.html', context)


@login_required(login_url='/admin/login/')
def delete_version(request, pk):
    """
    Delete a specific app version.
    """
    version = get_object_or_404(AppVersion, pk=pk)
    version.delete()
    return redirect('custom_admin')

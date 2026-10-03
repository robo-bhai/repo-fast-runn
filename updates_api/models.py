from django.db import models
import os

class AppVersion(models.Model):
    version_code = models.PositiveIntegerField(
        unique=True,
        help_text="Integer version code (e.g. 2, 3, 4). Must be higher than installed version."
    )
    version_name = models.CharField(
        max_length=50,
        help_text="Human-readable version (e.g. '1.1.0' or '2.0.0')"
    )
    apk_file = models.FileField(
        upload_to='apks/',
        help_text="Upload your compiled BatVoice APK file here"
    )
    release_notes = models.TextField(
        help_text="What's new in this release? (Bullet points recommended)",
        default="- Performance improvements\n- Battery health enhancements\n- Bug fixes"
    )
    file_size_mb = models.FloatField(
        default=0.0,
        blank=True,
        help_text="File size in MB (Automatically calculated on upload if left 0)"
    )
    force_update = models.BooleanField(
        default=False,
        help_text="If checked, users must update to continue using the app"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Only active versions are delivered to the Android app"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-version_code']
        verbose_name = 'App Release Version'
        verbose_name_plural = 'App Release Versions'

    def save(self, *args, **kwargs):
        if self.apk_file and (self.file_size_mb == 0.0 or not self.file_size_mb):
            try:
                self.file_size_mb = round(self.apk_file.size / (1024 * 1024), 2)
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"v{self.version_name} (Build {self.version_code}) - {'Active' if self.is_active else 'Inactive'}"

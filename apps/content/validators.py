import os
from django.core.exceptions import ValidationError

def validate_video_file(value):
    ext = os.path.splitext(value.name)[1]  # gets extension
    valid_extensions = [".mp4", ".mkv"]

    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file format. Only MP4 and MKV allowed.")

"""

def validate_video_file(value):
    valid_mime_types = ["video/mp4", "video/x-matroska"]

    file_mime = magic.from_buffer(value.read(1024), mime=True)

    if file_mime not in valid_mime_types:
        raise ValidationError("Invalid video file type.")

    value.seek(0)
    
    # Step 4 — Add File Size Limit (VERY IMPORTANT)
    def validate_video_file(value):
        max_size = 50 * 1024 * 1024  # 50 MB

        if value.size > max_size:
            raise ValidationError("File too large (max 50MB).")

"""
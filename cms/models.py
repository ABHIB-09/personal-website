from django.db import models

class MediaFile(models.Model):
    """Media library for CMS"""
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('document', 'Document'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='media_library/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    description = models.TextField(blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_public = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.name
    
    @property
    def file_extension(self):
        return self.file.name.split('.')[-1].lower() if '.' in self.file.name else ''
    
    @property
    def file_size(self):
        if self.file:
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
        return "0 B"
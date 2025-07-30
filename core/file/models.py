from django.db import models
from users.models import User

class UserFile (models.Model) : 
    name = models.CharField(max_length=225)
    content_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        related_name='userfile_owner',
        on_delete=models.CASCADE,
    )
    
    file_size_in_giga = models.FloatField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(
        User,
        related_name='userfile_shared_with',
        blank=True
    )

    file = models.FileField(
        upload_to='uploads',
        null=True,
        blank=True
    )

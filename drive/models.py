from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import filesizeformat


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='child_folders')

    folder_name = models.CharField(max_length=255)
    folder_date = models.DateTimeField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.folder_name


def validate_file_size(value):
    max_size = 100000000
    if value.size > max_size:
        raise ValidationError(f"The file size should not exceed {filesizeformat(max_size)}.")


class Files(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, default=0, null=True)
    file_name = models.CharField(max_length=255)
    file_upload = models.FileField(
        blank=True, null=True, upload_to='media/files', validators=[validate_file_size])
    upload_date = models.DateTimeField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name

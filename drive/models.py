from django.contrib.auth.models import User
from django.db import models


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='child_folders')

    folder_name = models.CharField(max_length=255)
    folder_date = models.DateTimeField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, through='Shared', related_name='shared_folders')

    def __str__(self):
        return self.folder_name


class Files(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, default=0, null=True)
    file_name = models.CharField(max_length=255)
    file_upload = models.FileField(
        blank=True, null=True, upload_to='media/files')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, through='Shared', related_name='shared_files')


class Shared(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(Files, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    shared_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.folder:
            return f"{self.user.username} shared {self.folder.folder_name}"
        elif self.file:
            return f"{self.user.username} shared {self.file.file_name}"
        else:
            return f"{self.user.username} shared item"


class UserPreference(models.Model):
    VIEW_MODE_CHOICES = (
        ('icon', 'Icon View'),
        ('table', 'Table View'),
    )
    THEME_MODE_CHOICES = (
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    view_mode = models.CharField(max_length=10, choices=VIEW_MODE_CHOICES)
    theme_mode = models.CharField(max_length=10, choices=THEME_MODE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"

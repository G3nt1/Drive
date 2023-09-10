from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    class Meta:
        verbose_name_plural = 'Folders'
        ordering = ['folder_date']


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

    class Meta:
        verbose_name_plural = 'Files'
        ordering = ['upload_date']


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

    class Meta:
        verbose_name_plural = 'Shared Items'
        ordering = ['shared_date']


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
    view_mode = models.CharField(max_length=10, choices=VIEW_MODE_CHOICES, null=True, blank=True, default='icon')
    theme_mode = models.CharField(max_length=10, choices=THEME_MODE_CHOICES, null=True, blank=True, default='light')

    def __str__(self):
        return f"Preferences for {self.user.username}"

    @receiver(post_save, sender=User)
    def create_user_preference(sender, instance, created, **kwargs):
        if created:
            UserPreference.objects.create(user=instance, view_mode='icon', theme_mode='light')

    post_save.connect(create_user_preference, sender=User)


class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    text_content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

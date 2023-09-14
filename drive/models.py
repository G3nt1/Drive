import os

import exifread
from PIL import Image
from PyPDF2 import PdfReader
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim


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
    file_upload = models.FileField(blank=True, null=True, upload_to='media/files')
    content = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, through='Shared', related_name='shared_files')

    # ...

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name_plural = 'Files'
        ordering = ['upload_date']


@receiver(post_save, sender=Files)
def extract_and_save_content(sender, instance, created, **kwargs):
    if created and instance.file_upload:
        file_path = instance.file_upload.path
        file_name, file_extension = os.path.splitext(instance.file_upload.name)

        # Check if it's an image file based on the file extension
        if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            # Extract image details
            try:
                file_size_bytes = os.path.getsize(file_path)
                file_size_mb = file_size_bytes / (1024 * 1024)

                image = Image.open(file_path)
                width, height = image.size
            except Exception as e:
                width, height = None, None

            # Extract image metadata if available (e.g., date and location)
            date_taken = None
            location_name = None
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                if 'EXIF DateTimeOriginal' in tags:
                    date_taken = tags['EXIF DateTimeOriginal']
                if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                    latitude = tags['GPS GPSLatitude'].values
                    longitude = tags['GPS GPSLongitude'].values
                    print(f"lat: {latitude} long: {longitude} ")
                    location_name = get_location_name(latitude, longitude)

                    # Update latitude and longitude fields
                    instance.latitude = convert_to_float(latitude)
                    instance.longitude = convert_to_float(longitude)

            # Update the instance with image details
            instance.content = f"Image Size: {width}x{height}\nFile Size: {file_size_mb:.2f} MB\nDate Taken: {date_taken}\nLocation: {location_name}"
            instance.save()
        elif file_extension.lower() in ['.txt', '.pdf']:
            # ... (rest of your code for handling text and PDF files)


            file_path = instance.file_upload.path
            if instance.file_upload.name.endswith('.txt'):
                # If it's a text file, read its content
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            elif instance.file_upload.name.endswith('.pdf'):
                # If it's a PDF file, extract its text content using PyPDF2
                pdf = PdfReader(file_path)
                content = ''
                for page in pdf.pages:
                    content += page.extract_text()

            # Save the extracted content to the instance
            instance.content = content
            instance.save()


def convert_to_float(coordinate):
    # Assuming coordinate is in the format [integer_part, numerator, denominator]
    integer_part, numerator, denominator = coordinate
    return float(integer_part) + (numerator / denominator)


def get_location_name(latitude, longitude):
    if latitude is not None and longitude is not None:
        try:
            geolocator = Nominatim(user_agent="myGeocoder")
            location = geolocator.reverse(f"{convert_to_float(latitude)}, {convert_to_float(longitude)}",
                                          exactly_one=True)

            if location:
                address = location.address
                country = location.raw.get("address", {}).get("country")
                return address, country
            else:
                return 'Location not found'
        except Exception as e:
            return 'Geocoding service error'
    return 'Latitude and longitude must be provided'


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

from django.contrib import admin

from .models import Files, Folder

# Register your models here.
admin.site.register(Folder),
admin.site.register(Files)

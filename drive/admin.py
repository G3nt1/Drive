from django.contrib import admin

from .models import Files, Folder, PDFDocument

# Register your models here.
admin.site.register(Folder),
admin.site.register(Files)
admin.site.register(PDFDocument)

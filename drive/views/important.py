from django.shortcuts import get_object_or_404, redirect

from drive.models import Folder, Files


def mark_important_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.is_important = True
    folder.save()
    return redirect('home')


def unmark_important_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.is_important = False
    folder.save()
    return redirect('home')


def mark_important_file(request, file_id):
    file = get_object_or_404(Files, id=file_id)
    file.is_important = True
    file.save()
    return redirect('home')


def unmark_important_file(request, file_id):
    file = get_object_or_404(Files, id=file_id)
    file.is_important = False
    file.save()
    return redirect('home')

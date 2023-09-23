from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from drive.models import Folder, Files


def delete_folder(folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.is_deleted = True
    folder.save()
    return redirect('home')


def restore_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.is_deleted = False
    folder.save()
    return redirect('home')


def delete_forever_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if folder.user == request.user:
        folder.delete()
        messages.success(request, "Folder deleted permanently.")
    else:
        messages.error(request, "You are not the owner of this file and cannot delete it.")

    return redirect('trash_list')

# Files
def delete_file(request, file_id):
    file = get_object_or_404(Files, id=file_id)
    file.is_deleted = True
    file.save()
    return redirect('home')


def restore_file(request, file_id):
    file = get_object_or_404(Files, id=file_id)
    file.is_deleted = False
    file.save()
    return redirect('home')


def delete_forever_files(request, file_id):
    file = get_object_or_404(Files, id=file_id)

    # Check if the logged-in user is the owner of the file
    if file.user == request.user:
        file.delete()
        messages.success(request, "File deleted permanently.")
    else:
        messages.error(request, "You are not the owner of this file and cannot delete it.")

    return redirect('trash_list')

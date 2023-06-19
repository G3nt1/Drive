import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from drive.forms import FolderForm, FileUploadForm
from drive.models import Folder, Files


def folder(request, folder_id):
    child_folders = Folder.objects.filter(user=request.user, is_deleted=False, parent_folder=folder_id)
    files = Files.objects.filter(folder_id=folder_id, is_deleted=False)
    return render(request, 'home.html', {
        'folders': child_folders,
        'folder': get_object_or_404(Folder, pk=folder_id, user=request.user),
        'files': files
    })


@login_required(login_url='login')
def create_folder(request, parent_folder_id=None):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.parent_folder_id = parent_folder_id
            new_folder.user = request.user
            new_folder.save()

            if parent_folder_id:
                return redirect('folder', folder_id=parent_folder_id)
            else:
                return redirect('home')
    else:
        form = FolderForm()

    return render(request, 'folder/create-new-folder.html', {'form': form})


def update_folder(request, folder_id):
    folders = Folder.objects.get(id=folder_id, user=request.user)
    if request.method == "POST":
        form = FolderForm(request.POST, instance=folders)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FolderForm(instance=folders)
    return render(request, 'folder/update_folder.html', {'form': form})


def upload_file(request, folder_id=None):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_upload')  # Get the list of uploaded files
            for file in files:
                file_upload = form.save(commit=False)
                file_upload.folder_id = folder_id
                file_upload.user = request.user
                file_upload.file_name = os.path.splitext(file.name)[0]
                file_upload.file_upload = file
                file_upload.save()
            return redirect('home')
    else:
        form = FileUploadForm()

    return render(request, 'files/upload-file.html', {'form': form})


def rename_files(request, file_id):
    files = Files.objects.get(id=file_id, user=request.user)

    if request.method == "POST":
        form = FileUploadForm(request.POST, instance=files)
        if form.is_valid():
            files.file_name = form.cleaned_data['file_name']
            files.save()
            return redirect('home')
    else:
        form = FileUploadForm(instance=files)

    return render(request, 'files/update-file.html', {'form': form, 'files': files, 'file_id': file_id})

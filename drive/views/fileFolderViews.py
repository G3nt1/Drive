from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from drive.forms import FolderForm, FileUploadForm
from drive.models import Folder, Files


def folder(request, folder_id):
    try:
        child_folders = Folder.objects.filter(user=request.user, is_deleted=False, parent_folder=folder_id)
        files = Files.objects.filter(folder_id=folder_id, is_deleted=False)
        return render(request, 'home.html', {
            'folders': child_folders,
            'files': files})
    except Folder.DoesNotExist:
        return HttpResponse("Folder not found.")


@login_required(login_url='login')
def create_folder(request, parent_folder_id=None):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            if parent_folder_id:
                parent_folder = Folder.objects.get(id=parent_folder_id, user=request.user)
                folder.parent_folder = parent_folder
                folder.save()
            else:
                # If no parent folder ID is provided, create a new parent folder
                folder.save()

            return redirect('home')
    else:
        form = FolderForm()

    return render(request, 'folder/create-new-folder.html', {'form': form, 'parent_folder_id': parent_folder_id})


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


def upload_file(request, folder_id):
    folders = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.folder = folders
            file_instance.save()
            return redirect('folder', folder_id=folder_id)
    else:
        form = FileUploadForm()

    return render(request, 'files/upload-file.html', {'form': form, 'folder': folders})


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

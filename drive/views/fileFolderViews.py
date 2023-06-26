import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from drive.forms import FolderForm, FileUploadForm, FileUpdateForm
from drive.models import Folder, Files, UserPreference


def get_theme_mode(request):
    user_preference = get_object_or_404(UserPreference, user=request.user)
    theme_mode = user_preference.theme_mode
    return theme_mode


def get_view_mode(request):
    user_preference = get_object_or_404(UserPreference, user=request.user)
    view_mode = user_preference.view_mode
    return view_mode


def folder(request, folder_id):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    parent_folder = get_object_or_404(Folder, pk=folder_id, user=request.user)
    child_folders = Folder.objects.filter(user=request.user, is_deleted=False, parent_folder=folder_id)
    files = Files.objects.filter(user=request.user, folder=parent_folder, is_deleted=False)
    return render(request, 'home.html', {
        'folders': child_folders,
        'folder': parent_folder,
        'files': files,
        'theme_mode': theme_mode,
        'view_mode': view_mode})


def files(request, file_id):
    file_instance = Files.objects.get(id=file_id)  # Replace <file_id> with the actual file ID
    file_size = file_instance.file_upload.file.size
    return render(request, 'home.html', {

        'files_size': file_size
    })


@login_required(login_url='login')
def create_folder(request, parent_folder_id=None):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
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

    return render(request, 'folder/create-new-folder.html', {'form': form,
                                                             'theme_mode': theme_mode,
                                                             'view_mode': view_mode})


def update_folder(request, folder_id):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    folders = Folder.objects.get(id=folder_id, user=request.user)
    if request.method == "POST":
        form = FolderForm(request.POST, instance=folders)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FolderForm(instance=folders)
    return render(request, 'folder/update_folder.html', {'form': form,
                                                         'theme_mode': theme_mode,
                                                         'view_mode': view_mode})


def upload_file(request, folder_id=None):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    if request.method == 'POST':
        files = request.FILES.getlist('file_upload')  # Get the list of uploaded files

        for file in files:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_upload = form.save(commit=False)
                file_upload.folder_id = folder_id
                file_upload.user = request.user
                file_upload.file_name = os.path.splitext(file.name)[0]
                file_upload.file_upload = file

                file_upload.save()

        return redirect('home')

    else:
        form = FileUploadForm()

    return render(request, 'files/upload-file.html', {'form': form,
                                                      'theme_mode': theme_mode,
                                                      'view_mode': view_mode})


def rename_files(request, file_id):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    files = Files.objects.get(id=file_id, user=request.user)

    if request.method == "POST":
        form = FileUpdateForm(request.POST, instance=files)
        if form.is_valid():
            files.file_name = form.cleaned_data['file_name']
            files.save()
            return redirect('home')
    else:
        form = FileUpdateForm(instance=files)

    return render(request, 'files/update-file.html', {'form': form, 'files': files, 'file_id': file_id,
                                                      'theme_mode': theme_mode,
                                                      'view_mode': view_mode})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from drive.forms import ShareFolderForm, ShareFileForm
from drive.models import Folder, Files, FolderShare, FileShare


@login_required
def share_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = ShareFolderForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user = get_object_or_404(User, email=user_id)

            folder_share = FolderShare(folder=folder, user=user)
            folder_share.save()

            return redirect('share_with_me', )
    else:
        form = ShareFolderForm()

    return render(request, 'share/share_folder.html', {'form': form, 'folder': folder})


@login_required
def share_file(request, file_id):
    file = get_object_or_404(Files, id=file_id)

    if request.method == 'POST':
        form = ShareFileForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user = get_object_or_404(User, email=user_id)

            file_share = FileShare(file=file, user=user)
            file_share.save()

            return redirect('share_with_me')
    else:
        form = ShareFileForm()

    return render(request, 'share/share_file.html', {'form': form, 'file': file})


@login_required
def share_with_me(request):
    shared_folders = FolderShare.objects.filter(user=request.user)
    shared_files = FileShare.objects.filter(user=request.user)

    return render(request, 'share/share_with_me.html', {'shared_folders': shared_folders, 'shared_files': shared_files})


@login_required
def open_shared_folder(request, folder_id):
    shared_folder = get_object_or_404(Folder, id=folder_id, is_deleted=False)
    return render(request, 'share/open_shared_folder.html', {'folder': shared_folder})

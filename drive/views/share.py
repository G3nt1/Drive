from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from drive.forms import SharedForm
from drive.models import Folder, Files, Shared


@login_required
def shared(request, pk):
    folder = get_object_or_404(Folder, id=pk)
    file = get_object_or_404(Files, id=pk)

    if request.method == 'POST':
        form = SharedForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user = get_object_or_404(User, email=user_id)

            folder_share = Shared(folder=folder, user=user)
            folder_share.save()
            file_share = Shared(file=file, user=user)
            file_share.save()
            return redirect('share_with_me')
    else:
        form = SharedForm()

    return render(request, 'share/share_items.html', {'form': form, 'folder': folder, 'file': file})


#
#
# @login_required
# def share_file(request, file_id):
#     file = get_object_or_404(Files, id=file_id)
#
#     if request.method == 'POST':
#         form = ShareFileForm(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data['user']
#             user = get_object_or_404(User, email=user_id)
#
#             file_share = FileShare(file=file, user=user)
#             file_share.save()
#
#             return redirect('share_with_me')
#     else:
#         form = ShareFileForm()
#
#     return render(request, 'share/share_file.html', {'form': form, 'file': file})
#
#
def share_with_me(request):
    shared_folders = Shared.objects.filter(folder__isnull=False)
    shared_files = Shared.objects.filter(file__isnull=False)

    return render(request, 'share/share_with_me.html', {'shared_folders': shared_folders, 'shared_files': shared_files})
#
#
# @login_required
# def open_shared_folder(request, folder_id):
#     shared_folder = get_object_or_404(Folder, id=folder_id, is_deleted=False)
#     return render(request, 'share/open_shared_folder.html', {'folder': shared_folder})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from drive.forms import SharedForm
from drive.models import Folder, Files, Shared


@login_required
def share_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        form = SharedForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user = get_object_or_404(User, email=user_id)
            folder_share = Shared(folder=folder, user=user)
            folder_share.save()

            return redirect('share_with_me')
    else:
        form = SharedForm()

    return render(request, 'share/share_items.html', {'form': form,
                                                      'folder': folder})


def share_file(request, file_id):
    file = get_object_or_404(Files, id=file_id, user=request.user)

    if request.method == 'POST':
        form = SharedForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user = get_object_or_404(User, email=user_id)

            file_share = Shared(file=file, user=user)
            file_share.save()
            return redirect('share_with_me')
    else:
        form = SharedForm()

    return render(request, 'share/share_items.html', {'form': form,
                                                      'file': file})


# views.py
def share_with_me(request):
    shared_folders = Shared.objects.filter(folder__isnull=False, user=request.user)
    shared_files = Shared.objects.filter(file__isnull=False, user=request.user)
    return render(request, 'share/share_with_me.html', {'shared_folders': shared_folders, 'shared_files': shared_files})

# @login_required
# def open_folder(request, folder_id):
#     shared_item = get_object_or_404(Shared, id=folder_id)
#
#     if shared_item.folder:
#         return render(request, 'share/open_shared.html', {'folder': shared_item.folder})
#     elif shared_item.file:
#         return render(request, 'share/open_shared.html', {'file': shared_item.file})
#     return redirect('share_with_me')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from drive.forms import SharedForm
from drive.models import Folder, Files, Shared, UserPreference


def get_theme_mode(request):
    user_preference = get_object_or_404(UserPreference, user=request.user)
    theme_mode = user_preference.theme_mode
    return theme_mode


def get_view_mode(request):
    user_preference = get_object_or_404(UserPreference, user=request.user)
    view_mode = user_preference.view_mode
    return view_mode


@login_required
def shared(request, pk):  # Add 'file_pk' as an argument
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    folder = get_object_or_404(Folder, id=pk, user=request.user)
    file = get_object_or_404(Files, id=pk, user=request.user)

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

    return render(request, 'share/share_items.html', {'form': form, 'folder': folder,
                                                      'file': file,
                                                      'theme_mode': theme_mode,
                                                      'view_mode': view_mode})


def share_with_me(request):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    shared_folders = Shared.objects.filter(
        folder__isnull=False, user=request.user)
    shared_files = Shared.objects.filter(file__isnull=False, user=request.user)

    return render(request, 'share/share_with_me.html', {'shared_folders': shared_folders,
                                                        'shared_files': shared_files,
                                                        'theme_mode': theme_mode,
                                                        'view_mode': view_mode
                                                        })


@login_required
def open_shared(request, pk):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    shared_item = get_object_or_404(Shared, id=pk)

    if isinstance(shared_item.folder, Folder):
        return render(request, 'share/open_shared.html', {'folder': shared_item.folder,
                                                          'theme_mode': theme_mode,
                                                          'view_mode': view_mode})
    elif isinstance(shared_item.file, Files):
        return render(request, 'share/open_shared.html', {'file': shared_item.file,
                                                          'theme_mode': theme_mode,
                                                          'view_mode': view_mode})

    return redirect('share_with_me')

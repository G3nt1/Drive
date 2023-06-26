from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from drive.forms import UserPreForm
from drive.models import Folder, Files, UserPreference


def get_theme_mode(request):
    user_preference = get_object_or_404(UserPreference, user=request.user)
    theme_mode = user_preference.theme_mode
    return theme_mode


def get_view_mode(request):
    user_preference = get_object_or_404(UserPreference, user=request.user)
    view_mode = user_preference.view_mode
    return view_mode


@login_required
def home(request):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)

    folders = Folder.objects.filter(user=request.user, is_deleted=False, parent_folder=None)
    files = Files.objects.filter(user=request.user, folder__isnull=True, is_deleted=False)

    if request.user.is_authenticated:
        # Save the session
        request.session.save()

    return render(request, 'home.html', {
        'folders': folders,
        'parent_folder_id': None,
        'active_menu': 'home',
        'files': files,
        'theme_mode': theme_mode,
        'view_mode': view_mode
    })


def trashItems(request):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)

    folders = Folder.objects.filter(user=request.user, is_deleted=True)
    files = Files.objects.filter(user=request.user, is_deleted=True)

    return render(request, 'trash/trash_list.html', {
        'folders': folders,
        'files': files,
        'active_menu': 'trash',
        'theme_mode': theme_mode,
        'view_mode': view_mode
    })


def important(request):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)

    important_files = Files.objects.filter(user=request.user, is_important=True)
    important_folders = Folder.objects.filter(user=request.user, is_important=True)

    return render(request, 'home.html', {
        'files': important_files,
        'folders': important_folders,
        'active_menu': 'important',
        'theme_mode': theme_mode,
        'view_mode': view_mode
    })


# Search views
def search(request):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    query = request.GET.get('query')
    if query:
        user = request.user
        results_folder = Folder.objects.filter(
            Q(folder_name__icontains=query) & Q(user=user)
        )
        results_files = Files.objects.filter(
            Q(file_name__icontains=query) & Q(folder__user=user)
        )
    else:
        results_folder = []
        results_files = []
    return render(request, 'home.html', {
        'folders': results_folder,
        'search_term': query,
        'files': results_files,
        'theme_mode': theme_mode,
        'view_mode': view_mode
    })


def user_preference(request):
    theme_mode = get_theme_mode(request)
    view_mode = get_view_mode(request)
    user_preference = get_object_or_404(UserPreference, user=request.user)

    if request.method == 'POST':
        form = UserPreForm(request.POST, instance=user_preference)
        if form.is_valid():
            user_preference = form.save(commit=False)
            theme_mode = request.POST.get('theme_mode', 'light')
            user_preference.theme_mode = theme_mode
            user_preference.save()
            return redirect('home')
    else:
        form = UserPreForm(instance=user_preference)

    return render(request, 'user_preference.html', {'form': form,
                                                    'theme_mode': theme_mode,
                                                    'view_mode': view_mode
                                                    })

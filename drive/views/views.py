from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from drive.forms import UserPreForm
from drive.models import Folder, Files, UserPreference


def get_theme_mode(request):
    if request.user.is_authenticated:
        user_preference = get_object_or_404(UserPreference, user=request.user)
        theme_mode = user_preference.theme_mode
    else:
        # Handle the case when the user is not authenticated
        theme_mode = None  # or any default value you prefer
    return {'theme_mode': theme_mode}


def get_view_mode(request):
    if request.user.is_authenticated:
        user_preference = get_object_or_404(UserPreference, user=request.user)
        view_mode = user_preference.view_mode
    else:
        view_mode = None
    return {'view_mode': view_mode}


#

@login_required
def home(request):
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

    })


def trashItems(request):
    folders = Folder.objects.filter(user=request.user, is_deleted=True)
    files = Files.objects.filter(user=request.user, is_deleted=True)

    return render(request, 'trash/trash_list.html', {
        'folders': folders,
        'files': files,
        'active_menu': 'trash',
    })


def important(request):
    important_files = Files.objects.filter(user=request.user, is_important=True)
    important_folders = Folder.objects.filter(user=request.user, is_important=True)

    return render(request, 'home.html', {
        'files': important_files,
        'folders': important_folders,
        'active_menu': 'important',
    })


# Search views
def search(request):
    query = request.GET.get('query')
    if query:
        user = request.user
        results_folder = Folder.objects.filter(
            Q(folder_name__icontains=query) & Q(user=user)
        )
        results_files = Files.objects.filter(file_name__icontains=query)

        results_content = Files.objects.filter(
            Q(content__icontains=query) & Q(user=user)
        )

    else:
        results_folder = []
        results_files = []
        results_content = []
    return render(request, 'home.html', {
        'folders': results_folder,
        'search_term': query,
        'files': results_files,
        'content': results_content
    })


def autocomplete(request):
    query = request.GET.get('query')
    user = request.user  # Make sure the user is authenticated

    if query:
        results_folder = Folder.objects.filter(folder_name__icontains=query)
        folder_name = [folder.folder_name for folder in results_folder]

        results_files = Files.objects.filter(file_name__icontains=query)
        file_name = [file.file_name for file in results_files]

        response_data = {
            'file_name': file_name,
            'folder_name': folder_name,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({}, safe=False)  # Return an empty JSON object if no results found


def user_preference(request):
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

                                                    })

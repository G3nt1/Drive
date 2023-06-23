from django.db.models import Q
from django.shortcuts import render, redirect

from drive.models import Folder, Files


def home(request):
    if request.method == 'POST':
        view = request.POST.get('view_mode', None)
        if view == 'table':
            request.session['view_mode'] = 'table'
            return redirect('home')
        elif view == 'icon':
            request.session['view_mode'] = 'icon'
            return redirect('home')

    top_level_folders = Folder.objects.filter(user=request.user, is_deleted=False, parent_folder=None)
    files = Files.objects.filter(user=request.user, folder__isnull=True, is_deleted=False)

    view_mode = request.GET.get('view_mode', 'table')

    if request.user.is_authenticated:
        # Save the session
        request.session.save()

    return render(request, 'home.html', {
        'folders': top_level_folders,
        'parent_folder_id': None,
        'active_menu': 'home',
        'files': files,
        'view_mode': view_mode
    })


def trashItems(request):
    folders = Folder.objects.filter(user=request.user, is_deleted=True)
    files = Files.objects.filter(user=request.user, is_deleted=True)

    return render(request, 'trash/trash_list.html', {
        'folders': folders,
        'files': files,
        'active_menu': 'trash'
    })


def important(request):
    important_files = Files.objects.filter(user=request.user, is_important=True)
    important_folders = Folder.objects.filter(user=request.user, is_important=True)

    return render(request, 'home.html', {
        'files': important_files,
        'folders': important_folders,
        'active_menu': 'important'
    })


# Search views
def search(request):
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
        'files': results_files
    })

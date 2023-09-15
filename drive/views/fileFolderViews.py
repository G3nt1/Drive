import os

import folium
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from drive.forms import FolderForm, FileUploadForm, FileUpdateForm
from drive.models import Folder, Files


def folder(request, folder_id):
    parent_folder = get_object_or_404(Folder, pk=folder_id, user=request.user)
    child_folders = Folder.objects.filter(user=request.user, is_deleted=False, parent_folder=folder_id)
    files = Files.objects.filter(user=request.user, folder=parent_folder, is_deleted=False)
    return render(request, 'home.html', {
        'folders': child_folders,
        'folder': parent_folder,
        'files': files,
    })


def files(request, file_id):
    file_instance = Files.objects.get(id=file_id)  # Replace <file_id> with the actual file ID
    file_size = file_instance.file_upload.file.size
    return render(request, 'home.html', {

        'files_size': file_size
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

    return render(request, 'folder/create-new-folder.html', {'form': form,
                                                             })


def update_folder(request, folder_id):
    folders = Folder.objects.get(id=folder_id, user=request.user)
    if request.method == "POST":
        form = FolderForm(request.POST, instance=folders)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FolderForm(instance=folders)
    return render(request, 'folder/update_folder.html', {'form': form,
                                                         })


def upload_file(request, folder_id=None):
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
                                                      })


def rename_files(request, file_id):
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
                                                      })


def display_image_location(request, file_id):
    try:
        file = Files.objects.get(id=file_id)

        # Check if the file has location information
        if file.latitude is not None and file.longitude is not None:
            latitude = file.latitude
            longitude = file.longitude

            # Create a Folium map centered around the image's location
            image_map = folium.Map(location=[latitude, longitude], zoom_start=15)

            # Add a marker for the image's location
            folium.Marker([latitude, longitude], tooltip="Image Location").add_to(image_map)

            # Convert the Folium map to HTML
            map_html = image_map._repr_html_()
        else:
            # If there is no location information, set map_html to an empty string
            map_html = ""

        context = {
            "file": file,
            "map_html": map_html,
        }

        return render(request, "files/images_details.html", context)

    except Files.DoesNotExist:
        # Handle the case where the file with the given ID doesn't exist
        return HttpResponse("File not found", status=404)


# views.py


def display_all_image_locations(request):
    try:
        # Retrieve all picture objects with valid location information
        pictures_with_location = Files.objects.exclude(latitude=None, longitude=None)

        # Create a Folium map
        image_map = folium.Map(location=[0, 0], zoom_start=2)  # Set initial map location and zoom level

        # Add markers for each picture's location
        for picture in pictures_with_location:
            latitude = picture.latitude
            longitude = picture.longitude
            marker = folium.Marker([latitude, longitude], tooltip=picture.file_name)
            marker.add_to(image_map)

        # Convert the Folium map to HTML
        map_html = image_map._repr_html_()

        context = {
            "map_html": map_html,
        }

        return render(request, "files/all_image_locations.html", context)

    except Exception as e:
        # Handle exceptions as needed
        return HttpResponse("Error: " + str(e), status=500)

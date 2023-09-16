import os
import zipfile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from drive.models import Folder


def export_all_files(request):
    # Get user folders
    user_folders = Folder.objects.filter(user=request.user)

    # Create the zip file
    zip_filename = 'exported_all_files.zip'
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # Add each folder and its contents to the zip
        for folder_obj in user_folders:
            folder_name = folder_obj.folder_name

            if folder_name:
                # Create a directory inside the zip file
                folder_path = folder_name + '/'
                zf.writestr(folder_path, '')

                # Add each file in the folder to the zip
                files_in_folder = Files.objects.filter(folder=folder_obj)
                for file_obj in files_in_folder:
                    file_path = file_obj.file_upload.path if file_obj.file_upload else None
                    if file_path:
                        zip_member_name = os.path.join(folder_name, os.path.basename(file_path))
                        zf.write(file_path, arcname=zip_member_name)

    with open(zip_path, 'rb') as zf:
        response = HttpResponse(zf.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(zip_filename)

    return response


def export_files_by_id(request, folder_id):
    # Get the specific folder by ID
    folder_obj = get_object_or_404(Folder, id=folder_id, user=request.user)

    # Create the zip file
    zip_filename = 'exported_folder_{}.zip'.format(folder_id)
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # Create a directory inside the zip file
        folder_path = folder_obj.folder_name + '/'
        zf.writestr(folder_path, '')

        # Add each file in the folder to the zip
        files_in_folder = Files.objects.filter(folder=folder_obj)
        for file_obj in files_in_folder:
            file_path = file_obj.file_upload.path if file_obj.file_upload else None
            if file_path:
                zip_member_name = os.path.join(folder_obj.folder_name, os.path.basename(file_path))
                zf.write(file_path, arcname=zip_member_name)

    with open(zip_path, 'rb') as zf:
        response = HttpResponse(zf.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(zip_filename)

    return response

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from drive.views import trashViews, fileFolderViews, authViews, views, zipfile, important

urlpatterns = [
    # # Trash
    path('trash/', views.trashItems, name='trash_list'),
    path('delete_folder/<int:folder_id>/', trashViews.delete_folder, name='delete_folder'),
    path('restore_folder/<int:folder_id>/', trashViews.restore_folder, name='restore_folder'),
    path('delete_forever_folder/<int:folder_id>/', trashViews.delete_forever_folder, name='delete_forever_folder'),

    path('delete_file/<int:file_id>/', trashViews.delete_file, name='delete_file'),
    path('restore_file/<int:file_id>/', trashViews.restore_file, name="restore_file"),
    path('delete_forever_file/<int:file_id>/', trashViews.delete_forever_files, name='delete_forever_file'),

    # Folder
    path('folder/create', fileFolderViews.create_folder, name="create_folder_root"),
    path('folder/create/<int:parent_folder_id>/', fileFolderViews.create_folder, name="create_folder"),
    path('', views.home, name='home'),
    path('folder/<int:folder_id>/', fileFolderViews.folder, name='folder'),
    path('update-folder/<int:folder_id>/',
         fileFolderViews.update_folder, name='update_folder'),
    # Files
    path('upload-file/<int:folder_id>/', fileFolderViews.upload_file, name='upload_file'),
    path('upload-file/', fileFolderViews.upload_file, name='upload_file_root'),
    path('rename-file/<int:file_id>/', fileFolderViews.rename_files, name='rename_files'),

    # Authenticated
    path('register/', authViews.register, name='register'),
    path('login/', authViews.user_login, name='user_login'),
    path('logout/', authViews.user_logout, name='user_logout'),

    # Search
    path('search', views.search, name='search'),

    path('important', views.important, name='is_important'),
    path('export-files/', zipfile.export_files, name='export_files'),

    path('mark_important_folder/<int:folder_id>', important.mark_important_folder, name='mark_folder'),
    path('unmark_important_folder/<int:folder_id>', important.unmark_important_folder, name='unmark_folder'),
    path('mark_important_file/<int:file_id>', important.mark_important_file, name='mark_file'),
    path('unmark_important_file/<int:file_id>', important.unmark_important_file, name='unmark_file'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

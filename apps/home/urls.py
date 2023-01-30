# -*- encoding: utf-8 -*-

from django.conf import settings
from django.urls import path, re_path
from apps.home import views
from django.conf.urls.static import static
# from .functions import remove_from_csv, edit_csv, edit_csv_and_dictionary
from apps.home import functions
# from .views import (
#     upload_statement,
# )

urlpatterns = [

    # The home page
    path('', views.upload_statement, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

    # views urls
    path('upload_statement/', views.upload_statement, name='upload_statement'),
    path('process_statement/', views.process_statement, name='process_statement'),
    path('download_csv/', views.download_csv, name='download_csv'),

    path('categories/', views.categories, name='categories'),

    path('categories_summary/', views.categories_summary, name='categories_summary'),

    path('statements_history/', views.statements_history, name='statements_history'),

    path('profile/', views.profile, name='profile'),


    # path('upload_csv_statement/', views.upload_csv_statement, name='upload_csv_statement'),

    # path('upload_statement_multiple/', views.upload_statement_multiple, name='upload_statement_multiple'),
    # path('categories_csv/', views.categories_csv, name='categories_csv'),

    # functions urls
    path('remove_from_csv/', functions.remove_from_csv, name='remove_from_csv'),
    path('edit_csv_and_dictionary/', functions.edit_csv_and_dictionary, name='edit_csv_and_dictionary'),
    path('edit_csv/', functions.edit_csv, name='edit_csv'),

    path('update_profile/', functions.update_profile, name='update_profile'),
    path('update_password/', functions.update_password, name='update_password'),
    path('delete_statement/', functions.delete_statement, name='delete_statement'),

    path('add_transaction/', functions.add_transaction, name='add_transaction'),
    path('generate_gfi/', functions.generate_gfi, name='generate_gfi'),
    path('update_category_summary_percentage/', functions.update_category_summary_percentage, name='update_category_summary_percentage')

    # path('upload_statement/', views.upload_statement, name='upload_statement'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

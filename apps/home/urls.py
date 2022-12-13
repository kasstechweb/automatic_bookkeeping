# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views

# from .views import (
#     upload_statement,
# )

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('upload_statement/', views.upload_statement, name='upload_statement'),
    path('process_statement/', views.process_statement, name='process_statement'),
    path('download_csv/', views.download_csv, name='download_csv'),

    path('categories/', views.categories, name='categories'),

    # path('upload_statement/', views.upload_statement, name='upload_statement'),
]

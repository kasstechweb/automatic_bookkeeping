# -*- encoding: utf-8 -*-

from django.conf import settings
from django.urls import path, re_path
from apps.home import views
from django.conf.urls.static import static
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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

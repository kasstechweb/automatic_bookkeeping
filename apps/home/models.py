# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from .functions import path_and_rename
# Create your models here.

# from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to=path_and_rename)
    # / 'documents/%Y/%m/%d'


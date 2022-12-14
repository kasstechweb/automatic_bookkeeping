# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from .functions import path_and_rename
# Create your models here.

# from django.db import models

class Document(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE,)
    docfile = models.FileField(upload_to=path_and_rename)
    # / 'documents/%Y/%m/%d'

class DictionaryCategories(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'dictionary_categories'


class DictionarySubcategories(models.Model):
    name = models.CharField(max_length=255)
    dictionary_category = models.ForeignKey(DictionaryCategories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dictionary_subcategories'
# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
# from .functions import path_and_rename
# Create your models here.

# from django.db import models
from .path_rename import path_and_rename

class Document(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE,)
    docfile = models.FileField(upload_to=path_and_rename)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # / 'documents/%Y/%m/%d'

class DictionaryCategories(models.Model):
    name = models.CharField(max_length=255)
    code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dictionary_categories'


class DictionarySubcategories(models.Model):
    name = models.CharField(max_length=255)
    dictionary_category = models.ForeignKey(DictionaryCategories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dictionary_subcategories'


class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'company'
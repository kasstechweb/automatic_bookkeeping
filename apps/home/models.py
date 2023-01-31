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
        ordering = ['id']

    def __str__(self):
        return self.name


class DictionarySubcategories(models.Model):
    name = models.CharField(max_length=255)
    dictionary_category = models.ForeignKey(DictionaryCategories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dictionary_subcategories'
        ordering = ['id']

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
class DictionarySubcategoriesNotApproved(models.Model):
    name = models.CharField(max_length=255)
    dictionary_category = models.ForeignKey(DictionaryCategories, models.DO_NOTHING)
    approved = models.BooleanField(choices=BOOL_CHOICES)

    class Meta:
        managed = False
        db_table = 'dictionary_subcategories_not_approved'
class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    yearend = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'
        ordering = ['id']
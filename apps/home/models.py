# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# from .functions import path_and_rename
# Create your models here.

# from django.db import models
from .path_rename import path_and_rename

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

def path_and_rename(instance, filename):
    upload_to = "statements"
    # print(instance)
    # ext = filename.split('.')[-1]
    # if filename.split('.')[-1] != 'pdf':
        # print('error pdf')
        # msg = 'error pdf'
    ext = 'pdf'
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
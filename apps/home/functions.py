import os
from pathlib import Path
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import User

import re
from django.http import JsonResponse

import requests
import pdfplumber
import pandas as pd
from collections import namedtuple
import csv
from unidecode import unidecode
from .models import DictionaryCategories, DictionarySubcategories

# from .views import get_category, get_all_sub_categories

# from apps.home.models import DictionaryCategories

def handle_uploaded_file(f):
    print('handling ' + settings.MEDIA_ROOT + f.name)
    destination = open(settings.MEDIA_ROOT + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

# def path_and_rename(instance, filename):
#     upload_to = "statements"
#     # print(instance)
#     # ext = filename.split('.')[-1]
#     # if filename.split('.')[-1] != 'pdf':
#         # print('error pdf')
#         # msg = 'error pdf'
#     ext = 'pdf'
#     # get filename
#     if instance.pk:
#         filename = '{}.{}'.format(instance.pk, ext)
#     else:
#         # set filename as random string
#         filename = '{}.{}'.format(uuid4().hex, ext)
#     # return the whole path to the file
#     return os.path.join(upload_to, filename)

# function to convert td bank pdf to csv file
def td_pdftocsv(request, file_name):
    current_user = request.user
    missing_category = False
    Inv = namedtuple('Inv', 'tr_date date description amount category')
    text = '' # new line
    with pdfplumber.open(settings.MEDIA_ROOT + "/" + str(file_name)) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text(x_tolerance=1, layout=False)
            text = text + '\n' + single_page_text

    inv_line_re = re.compile(r'((JAN?|FEB?|MAR?|APR?|MAY|JUN?|JUL?|AUG?|SEP?|OCT?|NOV?|DEC?)+ \d{1,2}) '
                         '((JAN?|FEB?|MAR?|APR?|MAY|JUN?|JUL?|AUG?|SEP?|OCT?|NOV?|DEC?)+ \d{1,2}) '
                         '([^\$]+)+ ([-]?[$]?\d{1,3}(?:,?\d{3})*\.\d{2})'
                        )

    # for line in text.split('\n'):
    #     line = inv_line_re.search(line)
    #     if line:
    #         # print(line)
    #         print(line.group(1) + ' * ' +line.group(3)+ ' * ' +line.group(5)+ ' * ' +line.group(6) )
    
    line_items = []
    for line in text.split('\n'):
        line = inv_line_re.search(line)
        if line:
            inv_dt = line.group(1)
            due_dt = line.group(3)
            desc = unidecode(line.group(5))
            inv_amt = line.group(6)
            sub_categories = DictionarySubcategories.objects.all()
            category = get_category(desc, sub_categories)
            if category == False:
                missing_category = True
            line_items.append(Inv(inv_dt, due_dt, desc, inv_amt, category))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv')
    return missing_category

#function to read csv file
def read_csv(file_path_name):
    file = open(file_path_name)
    csvreader = csv.reader(file)
    rows = []
    # d = dict()
    for row in csvreader:
        rows.append(row)
    # print (rows[1])
    # for r in rows:
    #     print(r[4]) 

    file.close()
    return rows


def get_category(search_str, sub_categories):
    # sub_categories = DictionarySubcategories.objects.all()
    search_str = search_str.lower()
    for x in sub_categories:
        if x.name.lower() in search_str:
            category = DictionaryCategories.objects.get(pk=x.dictionary_category_id)
            return category.name
    return False

# def get_sub_category(search_str, sub_categories):
#     search_str = search_str.lower()
#     for x in sub_categories:
#         if x[1] in search_str:
#             return x
#     return False

def remove_from_csv(request):
    # print('remove from csv called')
    # print(request.POST.get('id')) 
    # print(request.POST.get('file_name')) 
    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')))
    csv_file.drop(int(request.POST.get('id'))-1,axis=0,inplace=True)
    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False)
    data = {'status': 200,
            'deleted': 'test'}
    return JsonResponse(data)

def edit_csv_and_dictionary(request):
    print('edit csv called')
    print(request.POST.get('id'))
    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')))
    csv_file.at[int(request.POST.get('id'))-1,'description'] = request.POST.get('transaction')
    csv_file.at[int(request.POST.get('id'))-1,'amount'] = request.POST.get('amount')
    csv_file.at[int(request.POST.get('id'))-1,'category'] = request.POST.get('category')
    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False)
    # add to dictionary db
    category = DictionaryCategories.objects.get(name=request.POST.get('category'))
    print(category.pk)
    print(request.POST.get('transaction'))
    sub_category = DictionarySubcategories.objects.create(name=request.POST.get('transaction'), dictionary_category_id = category.pk)
    sub_category.save()
    data = {'status': 200,
            'msg': 'edit success!'
            }
    return JsonResponse(data)

def edit_csv(request):
    print('edit csv called')
    print(request.POST.get('id'))
    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')))
    csv_file.at[int(request.POST.get('id'))-1,'description'] = request.POST.get('transaction')
    csv_file.at[int(request.POST.get('id'))-1,'amount'] = request.POST.get('amount')
    csv_file.at[int(request.POST.get('id'))-1,'category'] = request.POST.get('category')
    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False)
    data = {'status': 200,
            'msg': 'edit success!'
            }
    return JsonResponse(data)
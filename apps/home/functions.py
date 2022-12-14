import os
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import User

import re

import requests
import pdfplumber
import pandas as pd
from collections import namedtuple
import csv
from unidecode import unidecode

# from apps.home.models import DictionaryCategories

def handle_uploaded_file(f):
    print('handling ' + settings.MEDIA_ROOT + f.name)
    destination = open(settings.MEDIA_ROOT + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

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

# function to convert td bank pdf to csv file
def td_pdftocsv(request, file_name):
    current_user = request.user
    Inv = namedtuple('Inv', 'tr_date date description amount')
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
            inv_amt = unidecode(line.group(5))
            desc = line.group(6)
            line_items.append(Inv(inv_dt, due_dt, inv_amt, desc))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv')

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
# # function to convert td bank pdf to csv file
# def get_categories(request, file_name):
    
    
#     # print(categories)
#     print('get cat')

# def get_sub_category(search_str, sub_categories):
#     search_str = search_str.lower()
#     for x in sub_categories:
#         if x[1] in search_str:
#             return x
#     return False
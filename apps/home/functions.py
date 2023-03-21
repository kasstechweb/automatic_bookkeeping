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
from .models import DictionaryCategories, DictionarySubcategories, Document, Company, DictionarySubcategoriesNotApproved

from datetime import datetime
import json
import openai

# from .views import get_category, get_all_sub_categories

# from apps.home.models import DictionaryCategories

def handle_uploaded_file(f):
    # print('handling ' + settings.MEDIA_ROOT + f.name)
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
    # Inv = namedtuple('Inv', 'tr_date date description amount category')
    text = '' # new line
    with pdfplumber.open(settings.MEDIA_ROOT + "/" + str(file_name)) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text(x_tolerance=1, y_tolerance=0, layout=False)
            text = text + '\n' + single_page_text

    inv_line_re = re.compile(r'((JAN?|FEB?|MAR?|APR?|MAY?|JUN?|JUL?|AUG?|SEP?|OCT?|NOV?|DEC?)\s\d{1,2})'
                             '\s((JAN?|FEB?|MAR?|APR?|MAY?|JUN?|JUL?|AUG?|SEP?|OCT?|NOV?|DEC?)\s\d{1,2})'
                             '\s([-]?[$]?\d{1,3}(?:,?\d{3})*\.\d{2})'
                             '\n?(([\*|\-|\_|A-Z|a-z|0-9]))?'
                             '\n(([a-zA-Z0-9].+)\s)'
                            '\n?(([\*|\-|\_|A-Z|a-z|0-9]\n)+)?'
                             '\n?(?!JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)([a-zA-Z0-9\-\_].+)?'
                        )


    # get previous balance
    opening_line_re = re.compile(r'(\bPREVIOUS STATEMENT BALANCE\b)\s(.?\d{1,3}(?:,?\d{3})*\.\d{2}.*?)')
    opening_line = opening_line_re.findall(text)
    opening_balance =  opening_line[0][1]
    opening_balance = opening_balance.replace('$', '')
    opening_balance = opening_balance.replace(',', '')
    previous_balance = float(opening_balance)
    # print(previous_balance)
    ignore_list = ['Available Credit', 'Cash Advances', 'CALCULATING YOUR BALANCE', 'Previous Balance', 'Payments & Credits', 'Interest', 'Sub-total']

    line_items = []
    sub_categories = DictionarySubcategories.objects.all()
    line = inv_line_re.findall(text)
    if line:
        for x in line:

            date = x[0]
            # get description but not in ignore
            for item in ignore_list:
                if x[11].find(item) != -1:
                    desc = unidecode(x[8])
                    break
                else:
                    desc = unidecode(x[8]) + ' ' + unidecode(x[11])

            amount = x[4].replace('$', '')
            amount = amount.replace(',', '')
            amount = float(amount)
            # print(amount)
            
            if amount > 0: #deposit
                deposited = ''
                withdrawn = amount
                balance = float(previous_balance) - withdrawn
                balance = round(balance, 2)
                balance = '%#.2f' % balance
                # balance = format(balance, '.2f')
            else:
                deposited = (amount * -1)
                withdrawn = ''
                balance = float(previous_balance) +  deposited
                balance = round(balance, 2)
                balance = '%#.2f' % balance
                # balance = format(balance, '.2f')
            previous_balance = balance

            
            category = get_category(desc, sub_categories)
            if category == False:
                missing_category = True

            line_items.append((date, desc, withdrawn, deposited, balance, category))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# function to convert rbc bank pdf to csv file
def rbc_pdftocsv(request, file_name):
    print('rbc_pdftocsv')
    missing_category = False
    Inv = namedtuple('Inv', 'ext_date date description amount category balance')
    text = '' # new line
    with pdfplumber.open(settings.MEDIA_ROOT + "/" + str(file_name)) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text(x_tolerance=1, y_tolerance=0,layout=False)
            text = text + '\n' + single_page_text

    text_match = re.compile(r"(\bOpening Balance|Opening balance\s\d{1,3}(?:,?\d{3})*\.\d{2}.*?\b)([\s\S]*)(\bClosing Balance|Closing balance\b)")
    text2 = text_match.findall(text)
    text2 = text2[0][1]

    # ignore_list = ['Opening Balance', 'Opening balance', 'Closing balance', 'Closing Balance', 'Total withdrawals', 'Total deposits', 'Total cheques', 'Balance', 'Serial', 'Account Fees']

    # lines = text.splitlines()
    ignore_list = [
        'Opening Balance', 
        'Opening balance', 
        'Closing balance', 
        'Closing Balance', 
        'Total withdrawals', 
        'Total deposits', 
        'Total cheques', 
        'Balance', 
        'Serial', 
        'Account Fees',
        'Your RBC',
        'Date Description',
        ]
    revenue_list = ['Deposit', 'deposit', 'ABM fee credit', 'Online Banking transfer', 'e-Transfer received']
    lines = text2.splitlines()
    previous_line = ''
    revenue = []    

    line_items = []
    sub_categories = DictionarySubcategories.objects.all()
    if lines:
        for line in lines:

            found_in_ignore = False
            for item in ignore_list:
                if line.find(item) != -1 or previous_line.find(item) != -1:
                    found_in_ignore = True
                    continue
            # skip small text
            if len(line) <= 5:
                continue
            # add previous lines in case of two lines
            if previous_line != '' and not found_in_ignore:
                line = previous_line + line
                previous_line = ''
            
            tr = rbc_transaction(line)

            if not tr:
                previous_line = line
                continue

            found_in_revenue = False
            for item in revenue_list:
                if tr[1].find(item) != -1:
                    found_in_revenue = True
                    revenue.append(tr[2])
                    continue
            if not found_in_revenue:
                date = tr[0]
                desc = tr[1]
                withdrawn = tr[2]
                balance = ''
                if len(tr) > 3:
                    balance = tr[3]
                category = get_category(desc, sub_categories)
                if category == False:
                    missing_category = True
                line_items.append((date, desc, withdrawn, '', balance, category))
                # print('==============================================================================')
                # print(tr)
    
    # calculate total revenue
    total_revenue = 0.0
    for x in revenue:
        x = x.replace(',', '')
        total_revenue = total_revenue + float(x)
        # print(x)
    line_items.append((date, 'Total Revenue', '', total_revenue, '', get_category('revenue', sub_categories)))
            # tr = rbc_transaction(line)
            # if len(tr) > 0:
            #     found_in_ignore = False
            #     for item in ignore_list:
            #         if tr[1].find(item) != -1:
            #             found_in_ignore = True
            #             continue
            #     if not found_in_ignore:
            #         date = tr[0]
            #         desc = tr[1]
            #         withdrawn = tr[2]
            #         balance = ''
            #         if len(tr) > 3:
            #             balance = tr[3]
            #         category = get_category(desc, sub_categories)
            #         if category == False:
            #             missing_category = True
            #         line_items.append((date, desc, withdrawn, 'deposited', balance, category))
            #         print("date: " + date + "desc: " + desc + "amount: " + withdrawn + "balance: " + balance)
    # inv_line_re = re.compile(r'(\d{1,2}\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))?\s?([a-zA-Z].+)(\s\d{1,3}(?:,?\d{3})*\.\d{2})(\s\d{1,3}(?:,?\d{3})*\.\d{2})'
    #                             '|(\d{1,2}\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))?\s?([a-zA-Z].+)(\s\d{1,3}(?:,?\d{3})*\.\d{2})'
    #                             '|(\d{1,2}\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))?\s?([a-zA-Z].+)\n(([\*|\-|\_|A-Z|a-z|0-9]\n)+)([a-zA-Z].+)(\s\d{1,3}(?:,?\d{3})*\.\d{2})(\s\d{1,3}(?:,?\d{3})*\.\d{2})'
    #                     )
    # ignore_list = ['Opening Balance', 'Opening balance', 'Closing balance', 'Closing Balance', 'Total withdrawals', 'Total deposits', 'Total cheques', 'Balance']

    # get opening balance
    # opening_line_re = re.compile(r'(\bOpening Balance\b|\bOpening balance\b)\s(.?\d{1,3}(?:,?\d{3})*\.\d{2}.*?)')
    # opening_line = opening_line_re.findall(text)
    # opening_balance =  opening_line[0][1]
    # opening_balance = opening_balance.replace(',', '')

    # line_items = []

    # for line in text.split('\n'):
        # restart = False
    # previous_balance = opening_balance
    # line = inv_line_re.findall(text)
    # if line:
    #     sub_categories = DictionarySubcategories.objects.all()

    #     for x in line:
    #         found = False
    #         for item in ignore_list:
    #             if x[7].find(item) != -1:
    #                 # desc = unidecode(x[8])
    #                 # print('found')
    #                 found = True
    #                 break
    #         if not found:
    #             if x[0] != '':
    #                 print(x[0]+ ' ========= ' + x[2] + ' ========= ' + x[3] + ' ========= ' + x[4])
    #                 # for item in ignore_list:
    #                 #     if x[2].find(item) != -1:
    #                 #         # desc = unidecode(x[8])
    #                 #         print(unidecode(x[2]))
    #                 #         break
    #                 #     else:
    #                 #         desc = unidecode(x[2])

    #                 date = x[0]
    #                 desc = unidecode(x[2])
    #                 amount = x[3]
    #                 balance = x[4]
                    
    #                 if balance > previous_balance: #deposit
    #                     deposited = amount
    #                     withdrawn = ''
    #                 else:
    #                     deposited = ''
    #                     withdrawn = amount
    #                 previous_balance = balance
                    
    #                 category = get_category(desc, sub_categories)
    #                 if category == False:
    #                     missing_category = True
    #                 line_items.append((date, desc, withdrawn, deposited, balance, category))

    #             elif x[5] != '' and x[0] == '' and x[1] == ''and x[2] == '' and x[3] == '' and x[4] == ''  :
    #                 # print(x[5]+ ' ========= ' + x[7] + ' ========= ' + x[8] + ' ========= ' + x[9])
    #                 date = x[5]
    #                 desc = x[7] 
    #                 amount = x[8]
    #                 balance = x[9]
                    
    #                 if balance > previous_balance: #deposit
    #                     deposited = amount
    #                     withdrawn = ''
    #                 else:
    #                     deposited = ''
    #                     withdrawn = amount
    #                 previous_balance = balance
                    
    #                 category = get_category(desc, sub_categories)
    #                 if category == False:
    #                     missing_category = True
    #                 line_items.append((date, desc, withdrawn, deposited, balance, category))

    #             elif x[2] != ''  and x[0] == '' and x[1] == '':
    #                 # print(' ========= ' + x[2] + ' ========= ' + x[3] + ' ========= ' + x[4])
    #                 date = ''
    #                 desc = x[2] 
    #                 amount = x[3]
    #                 balance = x[4]
                    
    #                 if balance > previous_balance: #deposit
    #                     deposited = amount
    #                     withdrawn = ''
    #                 else:
    #                     deposited = ''
    #                     withdrawn = amount
    #                 previous_balance = balance
                    
    #                 category = get_category(desc, sub_categories)
    #                 if category == False:
    #                     missing_category = True
    #                 line_items.append((date, desc, withdrawn, deposited, balance, category))

    #             elif x[11] != ''  and x[0] == '' and x[1] == '' and x[2] == '' and x[3] == '' and x[4] == ''and x[5] == ''and x[6] == ''and x[7] == '' and x[8] == ''and x[9] == ''and x[10] == '':
    #                 # print(' ========= ' + x[11] + ' ' + x[14] + ' ========= ' + x[15] + ' ========= ' + x[16])
    #                 date = ''
    #                 desc = x[11] + ' ' + x[14] 
    #                 amount = x[15]
    #                 balance = x[16]
                    
    #                 if balance > previous_balance: #deposit
    #                     deposited = amount
    #                     withdrawn = ''
    #                 else:
    #                     deposited = ''
    #                     withdrawn = amount
    #                 previous_balance = balance
                    
    #                 category = get_category(desc, sub_categories)
    #                 if category == False:
    #                     missing_category = True
    #                 line_items.append((date, desc, withdrawn, deposited, balance, category))

    #             elif x[9] != ''  and x[0] == '' and x[1] == '' and x[2] == '' and x[3] == '' and x[4] == ''and x[5] == ''and x[6] == ''and x[7] == '' and x[8] == '':
    #                 # print(x[9] + ' ========= ' + x[11] + ' ' + x[14] + ' ========= ' + x[15] + ' ========= ' + x[16])
    #                 date = x[9]
    #                 desc = x[11] + ' ' + x[14] 
    #                 amount = x[15]
    #                 balance = x[16]
                    
    #                 if balance > previous_balance: #deposit
    #                     deposited = amount
    #                     withdrawn = ''
    #                 else:
    #                     deposited = ''
    #                     withdrawn = amount
    #                 previous_balance = balance
                    
    #                 category = get_category(desc, sub_categories)
    #                 if category == False:
    #                     missing_category = True
    #                 line_items.append((date, desc, withdrawn, deposited, balance, category))

    #             elif x[7] != '' and x[0] == '' and x[1] == ''and x[2] == '' and x[3] == '' and x[4] == ''and x[5] == ''and x[6] == '':
    #                 # print(' ========= ' + x[7] + ' ========= ' + x[8] + ' ========= ' + x[9])
    #                 date = ''
    #                 desc = x[7]
    #                 amount = x[8]
    #                 balance = x[9]
                    
    #                 if balance > previous_balance: #deposit
    #                     deposited = amount
    #                     withdrawn = ''
    #                 else:
    #                     deposited = ''
    #                     withdrawn = amount
    #                 previous_balance = balance
                    
    #                 category = get_category(desc, sub_categories)
    #                 if category == False:
    #                     missing_category = True
    #                 line_items.append((date, desc, withdrawn, deposited, balance, category))


    # line_items = []
    # for line in text.split('\n'):
    #     restart = False
    #     line = inv_line_re.search(line)
    #     if line:
    #         # print(line)
    #         # for x in ignore_list:
    #             # print(x)
    #         for item in ignore_list:
    #             if str(line.group(2)).find(item) != -1:
    #                 # print(item)
    #                 restart = True
    #                 break
    #         if restart:
    #             continue
            
    #         ext_date = ''
    #         date = str(line.group(1))
    #         desc = line.group(2)
    #         amount = str(line.group(3))
    #         balance = str(line.group(4))

    #         sub_categories = DictionarySubcategories.objects.all()
    #         category = get_category(desc, sub_categories)
    #         if category == False:
    #             missing_category = True

    #         line_items.append(Inv(ext_date, date, desc, amount, category, balance))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# function to convert atb bank pdf to csv file
def atb_pdftocsv(request, file_name):
    # print('atb pdf called')
    missing_category = False
    # Inv = namedtuple('Inv', 'date_charged date_posted description amount category')
    text = '' # new line
    with pdfplumber.open(settings.MEDIA_ROOT + "/" + str(file_name)) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text(x_tolerance=1, layout=False)
            text = text + '\n' + single_page_text

    inv_line_re = re.compile(r'((Jan?|Feb?|Mar?|Apr?|May|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|Dec?)\s\d{1,2})\s'
                                '((Jan?|Feb?|Mar?|Apr?|May|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|Dec?)\s\d{1,2})\s'
                                '([a-zA-Z].+)\s(\d{1,3}(?:,?\d{3})*\.\d{2})$'
                            )

    line_items = []
    sub_categories = DictionarySubcategories.objects.all()
    for line in text.split('\n'):
        # restart = False
        line = inv_line_re.search(line)
        if line:
            
            date = line.group(1)
            # date_posted = line.group(3)
            desc = line.group(5)
            withdrawn = line.group(6)
            deposited = '' 
            balance = ''

            
            category = get_category(desc, sub_categories)
            if category == False:
                missing_category = True

            line_items.append((date, desc, withdrawn, deposited, balance, category))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# function to convert atb bank pdf to csv file
def servus_pdftocsv(request, file_name):
    missing_category = False
    # Inv = namedtuple('Inv', 'date tr_date description amount category balance')
    text = '' # new line
    with pdfplumber.open(settings.MEDIA_ROOT + "/" + str(file_name)) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text(x_tolerance=1, layout=False)
            text = text + '\n' + single_page_text

    inv_line_re = re.compile(r'((Jan?|Feb?|Mar?|Apr?|May|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|Dec?)\s\d{1,2})\s'
                                '(([a-zA-Z0-9].+)\s)(.?\d{1,3}(?:,?\d{3})*\.\d{2}.*?)\s(\d{1,3}(?:,?\d{3})*\.\d{2})$'
                            )

    line_items = []
    sub_categories = DictionarySubcategories.objects.all()
    for line in text.split('\n'):
        # restart = False
        line = inv_line_re.search(line)
        if line:
            
            date = line.group(1)
            desc = line.group(4)
            
            if '(' and ')' in str(line.group(5)):
                # print('withdrawl')
                withdrawn = line.group(5)
                deposited = ''
                withdrawn = clean_amount(withdrawn)
            else:
                # print('deposit')
                withdrawn = ''
                deposited = line.group(5)
                deposited = clean_amount(deposited)
                
            # amount = line.group(5)
            balance = line.group(6)
            balance = clean_amount(balance)

            category = get_category(desc, sub_categories)
            if category == False:
                missing_category = True

            line_items.append((date, desc, withdrawn, deposited, balance, category))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# function to convert atb bank pdf to csv file
def scotia_pdftocsv(request, file_name):
    missing_category = False
    Inv = namedtuple('Inv', 'date description withdrawn deposited balance category')
    text = '' # new line
    with pdfplumber.open(settings.MEDIA_ROOT + "/" + str(file_name)) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text(x_tolerance=1, y_tolerance=0, layout=False)
            text = text + '\n' + single_page_text

    inv_line_re = re.compile(r'((Jan?|Feb?|Mar?|Apr?|May?|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|Dec?)\s\d{1,2})\s(([a-zA-Z0-9].+)\s)(.?\d{1,3}(?:,?\d{3})*\.\d{2}.*?)\s([-]?\d{1,3}(?:,?\d{3})*\.\d{2})'
                        '\n?(([\*|\-|\_|A-Z|a-z|0-9]\n)+)?(?!Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)([a-zA-Z0-9\-\_].+)?'
                            )

    opening_line_re = re.compile(r'((Jan?|Feb?|Mar?|Apr?|May?|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|Dec?)\s\d{1,2})\s(\bOpening Balance\b)\s(.?\d{1,3}(?:,?\d{3})*\.\d{2}.*?)'
                        )

    opening_line = opening_line_re.findall(text)
    opening_balance =  opening_line[0][3]

    line_items = []
    sub_categories = DictionarySubcategories.objects.all()

    previous_balance = opening_balance
    line = inv_line_re.findall(text)
    if line:
        for x in line:
            date = x[0]
            desc = x[2] + x[8]
            desc = desc.strip()
            amount = x[4]
            balance = x[5]

            if balance > previous_balance: #deposit
                deposited = amount
                withdrawn = ''
            else:
                deposited = ''
                withdrawn = amount
            previous_balance = balance
            
            category = get_category(desc, sub_categories)
            if category == False:
                missing_category = True

            line_items.append(Inv(date, desc, withdrawn, deposited, balance, category))

    df = pd.DataFrame(line_items)

    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# function to read csv file and add categories and check if missing category
def td_process_csv(file_name):
    missing_category = False
    sub_categories = DictionarySubcategories.objects.all()
    transactions = read_csv(settings.MEDIA_ROOT + "/" + str(file_name))

    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/' + str(file_name)), header=None)
    csv_file[''] = ''
    for index, row in enumerate(transactions):
        # print(row[1])
        category = get_category(row[1], sub_categories)
        if category == False:
            missing_category = True
        csv_file.iat[index, 5] = category
    
    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/' + str(file_name)), index=False, header=None)
    return missing_category

# atb function to read csv file and add categories and check if missing category
def atb_process_csv(file_name):
    # print('atb csv called')
    missing_category = False
    sub_categories = DictionarySubcategories.objects.all()
    transactions = read_csv(settings.MEDIA_ROOT + "/" + str(file_name))
    del transactions[0]

    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/' + str(file_name)))
    line_items = []
    for row in transactions:
        # print(row[1])
        date = row[0]
        desc = row[8]
        withdrawn = row[5]
        deposited = row[6]
        balance = row[7]
        category = get_category(desc, sub_categories)
        if category == False:
            missing_category = True
        # csv_file.iat[index, 5] = category
        line_items.append((date, desc, withdrawn, deposited, balance, category))
    
    df = pd.DataFrame(line_items)
    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# rbc function to read csv file and add categories and check if missing category
def rbc_process_csv(file_name):
    missing_category = False
    sub_categories = DictionarySubcategories.objects.all()
    transactions = read_csv(settings.MEDIA_ROOT + "/" + str(file_name))
    del transactions[0]

    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/' + str(file_name)))
    line_items = []
    balance = 0.0
    for row in transactions:
        # print(row[1])
        date = row[2]
        desc = row[4]
        withdrawn = ''
        deposited = ''

        if float(row[6]) < 0: # withdrawl
            withdrawn = row[6]
        elif float(row[6]) > 0:
            deposited = row[6]

        balance = balance + float(row[6])
        balance = float("{:.2f}".format(balance))
        category = get_category(desc, sub_categories)
        if category == False:
            missing_category = True
        # csv_file.iat[index, 5] = category
        line_items.append((date, desc, withdrawn, deposited, balance, category))
    
    df = pd.DataFrame(line_items)
    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# cibc function to read csv file and add categories and check if missing category
def cibc_process_csv(file_name):
    missing_category = False
    sub_categories = DictionarySubcategories.objects.all()
    transactions = read_csv(settings.MEDIA_ROOT + "/" + str(file_name))
    # del transactions[0]

    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/' + str(file_name)))
    line_items = []
    balance = 0.0
    for row in transactions:
        # print(row[1])
        date = row[0]
        desc = row[1]
        withdrawn = row[2]
        deposited = row[3]

        if withdrawn == '':
            withdrawn = 0.0
        elif deposited == '':
            deposited = 0.0

        # print(withdrawn)
        
        balance = balance + float(withdrawn) + float(deposited)
        balance = float("{:.2f}".format(balance))

        category = get_category(desc, sub_categories)
        if category == False:
            missing_category = True
        # csv_file.iat[index, 5] = category
        line_items.append((date, desc, withdrawn, deposited, balance, category))
    
    df = pd.DataFrame(line_items)
    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
    return missing_category

# scotia function to read csv file and add categories and check if missing category
def scotia_process_csv(file_name):
    missing_category = False
    sub_categories = DictionarySubcategories.objects.all()
    transactions = read_csv(settings.MEDIA_ROOT + "/" + str(file_name))
    # del transactions[0]

    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/' + str(file_name)))
    line_items = []
    balance = 0.0
    for row in transactions:
        # print(row[1])
        date = row[0]
        if row[2] == '-':
            row[2] = ''
        desc = row[2] + row[3] + row[4]
        withdrawn = 0.00
        deposited = 0.00
        if float(row[1]) < 0:
            withdrawn = float(row[1])*(-1)
        else:
            deposited = row[1]

        # if withdrawn == '':
        #     withdrawn = 0.0
        # elif deposited == '':
        #     deposited = 0.0

        # print(withdrawn)
        
        balance = balance + float(withdrawn) + float(deposited)
        balance = float("{:.2f}".format(balance))

        category = get_category(desc, sub_categories)
        if category == False:
            missing_category = True
        # csv_file.iat[index, 5] = category
        if withdrawn == 0:
            withdrawn = ''
        if deposited == 0:
            deposited = ''
        line_items.append((date, desc, withdrawn, deposited, balance, category))
    
    df = pd.DataFrame(line_items)
    filename = str(file_name).rsplit('.', 1)[0]
    df.to_csv(settings.MEDIA_ROOT + "/"+ filename + '.csv', index=False, header=None)
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
    search_str = remove_digits(search_str)
    # print(search_str)
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
    # print('removing')
    # print(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')))
    # print(int(request.POST.get('id')))
    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), header=None)
    # print(csv_file)
    csv_file.drop(int(request.POST.get('id'))-1,axis=0,inplace=True)
    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False, header=None)
    data = {'status': 200,
            'deleted': 'test'}
    return JsonResponse(data)

def edit_csv_and_dictionary(request):

    # get dduplicates list
    file = open(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')))
    csvreader = csv.reader(file)
    original_transaction = request.POST.get('original_transaction')
    transaction = request.POST.get('transaction')
    duplicates_ids = []

    for index, row in enumerate(csvreader):
        if remove_digits(transaction) in remove_digits(row[1]):
            duplicates_ids.append(index)
    file.close()
    
    # read csv with pandas and update caategories imcluding duuplicates
    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), header=None)
    for dup in duplicates_ids:
        csv_file.iat[int(dup), 5] = request.POST.get('category') # 5 is category column
    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False, header=None)

    # add to dictionary db
    category = DictionaryCategories.objects.get(name=request.POST.get('category'))
    check_sub_category = DictionarySubcategoriesNotApproved.objects.filter(name= remove_digits(transaction)).exists()
    if not check_sub_category: # not found duplicate
        sub_category = DictionarySubcategoriesNotApproved.objects.create(name= remove_digits(transaction), dictionary_category_id = category.pk, approved=0)
        sub_category.save()

    data = {'status': 200,
            'msg': 'edit success!',
            'duplicates_ids': duplicates_ids
            }
    return JsonResponse(data)

def ai_get_category(request):
    
    # # get dduplicates list
    # file = open(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')))
    # csvreader = csv.reader(file)
    # # original_transaction = request.POST.get('original_transaction')
    transaction = request.POST.get('transaction')
    transaction = remove_extras_ai(transaction)
    # Set up the OpenAI API client
    openai.api_key = "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"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt = "categorize this bank transaction \"" + transaction + "\","
    prompt = prompt + "choose from: Accounting fees,Advertising,Advertising and promotion,Amortization of intangible assets,Amortization of natural resource assets,Amortization of tangible assets,Appraisal fees,Architect Fees,Bad debt expense,Bank charges,Bonuses,Brokerage fees,Business taxes,Business taxes, licences and memberships,Camp supplies,Cash over / short,Collection and credit costs,Commissions,Computer-related expenses,Condominium fees,Consulting fees,Contributions to deferred income plans,Credit card charges,Crew share,Data processing,Delivery, freight and express,Directors fees,Donations,Dumping charges,Electricity,Employee benefits,Employee salaries,Employer's portion of employee benefits,Equipment rental,Fishing gear,Food and catering,Franchise fees,Fuel costs,Garbage removal,General and administrative expenses,Goodwill impairment loss,Government fees,Group insurance benefits,Heat,Insurance,Interest and bank charges,Interest on bonds and debentures,Interest on long term debt,Interest on mortgages,Interest on short term debt,Interest paid (financial institutions),Interest paid on bonds and debentures,Interest paid on deposits,Interfund transfer,Internet,Laboratory fees,Land fill fees,Laundry,Legal fees,Life insurance on executives,Loan losses,Machine shop expense,Management and administration fees,Management salaries,Meals and entertainment,Medical fees,Meetings and conventions,Memberships,Moorage (boat),Motor vehicle rentals,Nets and traps,Nova Scotia tax on large corporations,Occupancy costs,Office stationery and supplies,Office utilities,Other expenses,Other repairs and maintenance,Professional fees,Promotion,Property taxes,Provision for loan losses,Quota rental,Real estate rental,Refining and assay,Registrar and transfer agent fees,Reimbursement of parent company expense,Rental,Repairs and maintenance,Repairs and maintenance - boats,Repairs and maintenance - buildings,Repairs and maintenance - machinery and equipment,Repairs and maintenance - vehicles,Research and development,Restructuring costs,Road costs,Royalty expenses - non-resident,Royalty expenses - resident,Salaries and wages,Salt, bait, and ice,Securities and commission fees,Security,Selling expenses,Shipping and warehouse expense,Shop expense,Small tools,Storage,Studio and recording,Sub-contracts,Supplies,Telephone and telecommunications,Training expense,Transfer fees,Travel expenses,Uniforms,Upgrade,Utilities,Vehicle expenses,Veterinary fees,Water,Warranty expenses,Withholding taxes,Cost of Good Sold,Office expenses,Motor Vehicles,Payment."
    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1,
    )

    response = completion.choices[0].text
    response = response.lstrip()
    response = response.rstrip()
    print(remove_extras_ai(transaction))
    print(response)
    # # ai code

    # duplicates_ids = []

    # for index, row in enumerate(csvreader):
    #     if remove_digits(transaction) in remove_digits(row[1]):
    #         duplicates_ids.append(index)
    # file.close()
    
    # # read csv with pandas and update caategories imcluding duuplicates
    # csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), header=None)
    # for dup in duplicates_ids:
    #     csv_file.iat[int(dup), 5] = request.POST.get('category') # 5 is category column
    # csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False, header=None)

    # # add to dictionary db
    # category = DictionaryCategories.objects.get(name=request.POST.get('category'))
    # check_sub_category = DictionarySubcategoriesNotApproved.objects.filter(name= remove_digits(transaction)).exists()
    # if not check_sub_category: # not found duplicate
    #     sub_category = DictionarySubcategoriesNotApproved.objects.create(name= remove_digits(transaction), dictionary_category_id = category.pk, approved=0)
    #     sub_category.save()

    data = {'status': 200,
            'msg': 'edit success!',
            'response': response,
            # 'duplicates_ids': duplicates_ids
            }
    return JsonResponse(data)

def edit_csv(request):
    # print('edit csv called')
    # print(request.POST.get('id'))
    csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), header=None)

    csv_file.iat[int(request.POST.get('id'))-1, 1] = request.POST.get('transaction')
    csv_file.iat[int(request.POST.get('id'))-1, 2] = request.POST.get('withdrawn')
    csv_file.iat[int(request.POST.get('id'))-1, 3] = request.POST.get('deposited')
    csv_file.iat[int(request.POST.get('id'))-1, 4] = request.POST.get('balance')
    csv_file.iat[int(request.POST.get('id'))-1, 5] = request.POST.get('category')

    csv_file.to_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), index=False, header=None)
    data = {'status': 200,
            'msg': 'edit success!'
            }
    return JsonResponse(data)

def remove_digits(str):
    # str = str.split('*')[0]
    clean_str = re.sub('\w*\d|\*.*\w.*', '', str)
    # clean_str = re.sub('[\d\-\*]', ' ', str)
    clean_str = clean_str.rstrip()
    clean_str = clean_str.rstrip("FROM: /-")
    return clean_str

def remove_extras_ai(str):
    # str = str.split('*')[0]
    clean_str = re.sub('[\d\-\*]', ' ', str)
    clean_str = clean_str.rstrip()
    clean_str = clean_str.rstrip("FROM: /-")
    return clean_str

def clean_amount(str):
    new_str = str
    new_str = new_str.replace(',', '')
    new_str = new_str.replace('$', '')
    new_str = new_str.replace('(', '')
    new_str = new_str.replace(')', '')
    
    return new_str

def path_and_rename(ext):
    upload_to = "statements"
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def update_profile(request):
    # print(request.POST.get('user_id'))
    user_id = request.POST.get('user_id')
    user = User.objects.get(pk = user_id)
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.save()
    # user.comp_name = request.POST.get('comp_name')
    if Company.objects.filter(user_id = user_id).exists():
        # print('exists')
        company = Company.objects.get(user_id = user_id)
        company.name = request.POST.get('comp_name')
        company.phone = request.POST.get('phone')
        company.street = request.POST.get('street')
        company.city = request.POST.get('city')
        company.province = request.POST.get('province')
        company.zip = request.POST.get('zip')
        company.yearend = request.POST.get('yearend')
        company.save()
    else:
        Company.objects.create(
            user_id = request.POST.get('user_id'), 
            name = request.POST.get('comp_name'),
            phone = request.POST.get('phone'),
            street = request.POST.get('street'),
            city = request.POST.get('city'),
            province = request.POST.get('province'),
            zip = request.POST.get('zip')
            )
    # print(user.comp_name)
    

    data = {'status': 200,
            'msg': 'update username/email success!'
            }
    return JsonResponse(data)

def update_password(request):
    # print(request.POST.get('user_id'))
    
    # user.username = request.POST.get('username')
    # user.email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if password == confirm_password:
        user = User.objects.get(pk = request.POST.get('user_id'))
        user.set_password(password)
        user.save()
        data = {'status': 200,
            'msg': 'change password success!'
            }
        return JsonResponse(data)
    else:
        data = {'status': 400,
            'msg': 'The two password fields didn’t match!'
            }
        return JsonResponse(data)
    
def delete_statement(request):
    # print(request.POST.get('file_id'))
    file_id = request.POST.get('file_id')
    document = Document.objects.get(pk=file_id)
    file_path_name = document.docfile
    # print(file_path_name)
    gfi_file = str(file_path_name).rsplit('\\', 1)[1]
    gfi_file = str(gfi_file).rsplit('.', 1)[0] + '.gfi'
    percentage_file = str(gfi_file).rsplit('.', 1)[0] + '_percent.txt'
    csv_path = Path(settings.MEDIA_ROOT + str(file_path_name))
    gfi_path = Path(settings.MEDIA_ROOT + '/statements/' + str(gfi_file))
    percent_path = Path(settings.MEDIA_ROOT + '/statements/' + str(percentage_file))
    # print(gfi_file)
    if csv_path.exists():
        os.remove(csv_path)
    if gfi_path.exists():
        os.remove(gfi_path)
    if percent_path.exists():
        os.remove(percent_path)
    # Document.objects.filter(pk=file_id).delete()
    document.delete()

    data = {'status': 200,
            'msg': 'change password success!'
            }
    return JsonResponse(data)

def add_transaction(request):
    # print(request.POST.get('file_name'))
    # print("add category requested")
    file_name = request.POST.get('file_name')
    date = request.POST.get('date')
    new_date = datetime.strptime(date, '%Y-%m-%d')
    day = new_date.strftime("%d")
    month = new_date.strftime("%b")
    final_date = day + '-' + month
    # print(day + '-' + month)
    transaction = request.POST.get('transaction')
    category = request.POST.get('category')
    withdrawn = request.POST.get('withdrawn')
    deposited = request.POST.get('deposited')
    balance = request.POST.get('balance')
    data = [
        [final_date, transaction, withdrawn, deposited, balance, category]
    ]
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(settings.MEDIA_ROOT + '/statements/' + file_name, mode='a', index=False, header=None)

    # csv_file = pd.read_csv(Path(settings.MEDIA_ROOT + '/statements/' +request.POST.get('file_name')), header=None)

    data = {'status': 200,
            'msg': 'add success!'
            }
    return JsonResponse(data)

def categories_percent_read(file_name):
    # print('categories_percentage called')
    file_name = Path(settings.MEDIA_ROOT + '/statements/' + file_name +  str('_percent.txt'))
    # mode = 'a' if os.path.exists(file_name) else 'w'
    with open(file_name, 'r') as f: 
        file_contents = f.read()
        # print(s)
    # print(file_contents)

def categories_percent_write(file_name, category, percent):
    # print('categories_percentage write called')
    category -= 1
    file_name = Path(settings.MEDIA_ROOT + '/statements/' + file_name +  str('_percent.txt'))
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write('')
    # mode = 'a' if os.path.exists(file_name) else 'w'
    with open(file_name, 'r') as file:
    # read a list of lines into data
        data = file.readlines()

    # print(data)
    # print(category)
    # print("len data: " + str(len(data)))
    # print("data category: " + str(category) + data[category])
    if len(data) < category+1:
        data.append(str(percent) + '\n')
    else:
        data[category] = str(percent) + '\n'

    with open(file_name, 'w') as file:
        file.writelines(data)

def update_category_summary_percentage(request):
    # print('update_category_summary_percentage called')
    category = int(request.POST.get('category'))
    new_filename = request.POST.get('new_filename')
    percentage = request.POST.get('percentage')

    categories_percent_write(new_filename, category, percentage)
    data = {'status': 200,
        'msg': 'percentage updated!'
        }
    return JsonResponse(data)

def generate_gfi(request):
    # for x in summary:
    #     print(x)
    current_user = request.user
    # print(current_user.id)
    company_details = Company.objects.get(user_id = current_user.id)

    line = '"GIFI01","","","","","Intuit Inc.","","","","","QuickBooks Online","","",'
    line += '"' + str(company_details.phone) + '",'
    line += '"' + str(company_details.name) + '",'
    line += '"' + str(company_details.street) + '",'
    line += '"' + str(company_details.city) + '",'
    line += '"' + str(company_details.province) + '",'
    line += '"' + str(company_details.zip) + '",'
    line += '"","","",""'
    line += '\n'

    # new_filename = str(file_name).rsplit('.', 1)[0]
    new_filename = request.POST.get('new_filename')
    # summary = request.POST.get('summary')

    transactions = read_csv(Path(settings.MEDIA_ROOT + '/statements/' + new_filename + '.csv') )
    categories = DictionaryCategories.objects.all()
    summary = []
    for cat in categories:
        duplicates = []
        for index,tr in enumerate(transactions):
            # print(tr)
            if cat.name == tr[5]:
                duplicates.append(index)
        
        withdrawn = 0.00
        deposited = 0.00
        for dup in duplicates:
            # print(transactions[dup][2])
            if transactions[dup][2] != '':
                amount = clean_amount(transactions[dup][2])
                withdrawn += float(amount)
            if transactions[dup][3] != '':
                amount = clean_amount(transactions[dup][3])
                deposited += float(amount)
        # print('>> ' + str(num1) + ' ' + str(num2))
        
        # # format floats to 2 decimals
        # withdrawn = format(withdrawn, '.2f')
        # deposited = format(deposited, '.2f')
        # print(withdrawn)
        # if cat.name in transactions:
        if withdrawn != 0.00 or deposited != 0.00:
            summary.append([cat.name, format(withdrawn, '.2f'), format(deposited, '.2f')])

    percentage_file = Path(settings.MEDIA_ROOT + '/statements/' + new_filename +  str('_percent.txt'))
    if not os.path.exists(percentage_file):
        for index, x in enumerate(summary):
            # print(index+1)
            categories_percent_write(new_filename, index+1, 100)
        # print(x)
    else:
        with open(percentage_file, 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        data = list(map(lambda x:x.strip(),data))
        # print(data)
        for index, row in enumerate(data):
            # print(row)
            summary[index].append(row)
    # print(new_filename)
    # print(summary) 
    # print(type(summary)) 
    with open(settings.MEDIA_ROOT + '/statements/' + new_filename + ".gfi", "w") as f:
        for row in summary:
            # print(row)
            category = row[0]
            categories = DictionaryCategories.objects.get(name = category)
            code = categories.code
            percentage = float(row[3]) / 100.00

            if code != 0:
                withdrawn = row[1]
                deposited = row[2]
                line += '"' + str(code) + '",'
                if withdrawn != '0.00':
                    # print(withdrawn)
                    # print(type(withdrawn))
                    # print(percentage)
                    # print(type(percentage))
                    amount = float(withdrawn) * percentage
                    line += str('%#.2f' % amount) + '\n'
                if deposited != '0.00':
                    # print(deposited)
                    amount = float(deposited) * percentage
                    line += str('%#.2f' % amount) + '\n'
                f.write(line)
            line = ''

    data = {'status': 200,
            'msg': 'add success!'
            }
    return JsonResponse(data)

def update_subcategories(obj):
    # print(subcategory_approved.name)
    subcategory_approved = DictionarySubcategoriesNotApproved.objects.get(pk = obj.id)
    check_sub_category = DictionarySubcategoriesNotApproved.objects.filter(name= remove_digits(subcategory_approved.name)).exists()
    if not check_sub_category: # not found duplicate
        sub_category = DictionarySubcategories.objects.create(name= remove_digits(subcategory_approved.name), dictionary_category_id = subcategory_approved.dictionary_category_id)
        sub_category.save()
    # print(subcategory_approved.name)
    # print('update_subcategories called')


def rbc_transaction(mystr):
    mystr = mystr.lstrip()
    transaction = []
    date_pattern = re.compile("((\d{1,2})\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))")  # type Pattern[str]
    amount_pattern = re.compile('-?[0-9,]+\.[0-9]{2}')
    
    date_match = re.findall(date_pattern, mystr)
    amount_match = re.findall(amount_pattern, mystr)
    
    if date_match:
        transaction.append(date_match[0][0]) # add date to transaction
        transaction_desc = re.sub(date_match[0][0], '', mystr) # remove date
        if len(amount_match) == 0:
            transaction.append(transaction_desc)
    else:
        transaction_desc = mystr
        
    # if amount more than two ignore the first
    if len(amount_match) == 3:
        transaction_desc = re.sub(amount_match[1], '', transaction_desc) # remove amount 0
        transaction_desc = re.sub(amount_match[2], '', transaction_desc) # remove amount 1   
        transaction_desc = transaction_desc.rstrip()
        transaction_desc = transaction_desc.lstrip()
        
        if not date_match:
            transaction.append('')
        transaction.append(transaction_desc)
        transaction.append(amount_match[1])
        transaction.append(amount_match[2])
        
    elif len(amount_match) == 1: #only one amount found
        transaction_desc = re.sub(amount_match[0], '', transaction_desc) # remove amount 0
        transaction_desc = transaction_desc.rstrip()
        transaction_desc = transaction_desc.lstrip()

        if len(transaction_desc) == 0: # there is amount but no desc 
            return False
        
        if not date_match:
            transaction.append('')
        transaction.append(transaction_desc)
        transaction.append(amount_match[0])
        
    elif len(amount_match) == 2: # two amount found:
        transaction_desc = re.sub(amount_match[0], '', transaction_desc) # remove amount 0
        transaction_desc = re.sub(amount_match[1], '', transaction_desc) # remove amount 1   
        transaction_desc = transaction_desc.rstrip()
        transaction_desc = transaction_desc.lstrip()
        
        if not date_match:
            transaction.append('')
        transaction.append(transaction_desc)
        transaction.append(amount_match[0])
        transaction.append(amount_match[1])
        
    elif len(amount_match) == 0 and mystr != '': # two amount found:
        return False
    return transaction
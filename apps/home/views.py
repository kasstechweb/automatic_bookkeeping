# -*- encoding: utf-8 -*-

from pathlib import Path
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings

from .models import DictionaryCategories, DictionarySubcategories, Document

# from django.shortcuts import render  
from .forms import DocumentForm, DocumentCSVForm, DocumentMultipleForm
from django.shortcuts import render
from apps.home import functions, path_rename
import ast
import pandas as pd
# td_pdftocsv, rbc_pdftocsv, atb_pdftocsv, servus_pdftocsv, scotia_pdftocsv, read_csv, td_process_csv


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Upload statement page and go to process statement page 
@login_required(login_url="/login/")
def upload_statement(request):
    context = {'segment': 'upload_statement'}
    msg = ''
    current_user = request.user
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            # print(request.POST.get('bank'))
            bank = request.POST.get('bank')
            # print(request.FILES)
            if request.FILES['docfile'].name.split('.')[-1] != 'pdf':
                # print('error pfd')
                msg = 'Unsupported file extension, please upload a .pdf statement'
            else:
                newdoc = Document(docfile = request.FILES['docfile'])
                newdoc.submitter = request.user
                # print(newdoc)
                newdoc.save()
                # print(newdoc.docfile)
                return render(request, 'home/process_statement.html', 
                    {
                    'user_id': current_user.id,
                    'file_id': newdoc.pk, 
                    'bank': bank
                    })
        # handle_uploaded_file(request.FILES['statement_file'])
        # statement_file = request.FILES['statement_file']
        # return HttpResponse('the name is '+ str(statement_file))
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        # html_template = loader.get_template('home/upload_statement.html' )
        # return HttpResponse(html_template.render(context, request))
        form = DocumentForm(request.POST, request.FILES)
        return render(request, 'home/upload_statement.html', {'segment': 'upload_statement' ,'form': form, 'msg':msg})

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# process statement page and go to download page 
@login_required(login_url="/login/")
def process_statement(request):
    context = {}
    current_user = request.user
    # if request.method == "POST":
        # print('process statement post called')
        # print(file_name)
        # return HttpResponse(file_name)
    try:
        # form = DocumentForm(request.POST, request.FILES)
        # td_pdftocsv(request)
        return render(request, 'home/process_statement.html', 
            {
            'user_id': current_user.id
            })

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# download csv page and go to categories page
@login_required(login_url="/login/")
def download_csv(request):
    context = {}
    if request.method == "POST":
        print('download_csv post called')
        # file_id = request.POST.get('file_id')
        # check banks
        bank = request.POST.get('bank')
        files_ids = request.POST.get('files_ids')
        files_ids = ast.literal_eval(files_ids)
        print(type(files_ids))
        print(files_ids)
        missing_category_list = []
        for file_id in files_ids:
            print(file_id)
            file = Document.objects.get(pk=file_id)
            file_name = file.docfile
            print(str(file_name).rsplit('.', 1)[1])
            file_ext = str(file_name).rsplit('.', 1)[1]

            if file_ext == 'pdf':
                if bank == 'td':
                    check_missing_category = functions.td_pdftocsv(request, file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'rbc':
                    check_missing_category = functions.rbc_pdftocsv(request, file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'atb':
                    check_missing_category = functions.atb_pdftocsv(request, file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'servus':
                    check_missing_category = functions.servus_pdftocsv(request, file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'scotia':
                    check_missing_category = functions.scotia_pdftocsv(request, file_name)
                    missing_category_list.append(check_missing_category)
            elif file_ext == 'csv':
                if bank == 'td':
                    check_missing_category = functions.td_process_csv(file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'atb':
                    check_missing_category = functions.atb_process_csv(file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'rbc':
                    check_missing_category = functions.rbc_process_csv(file_name)
                    missing_category_list.append(check_missing_category)
                elif bank == 'cibc':
                    check_missing_category = functions.cibc_process_csv(file_name)
                    missing_category_list.append(check_missing_category)
            
            
        
        if True in missing_category_list: # there is a missing category ask user to add it before downloading csv
            print('there is missing category')
            # file_id = request.POST.get('file_id')
            print(files_ids)
            # files_ids = request.POST.get('files_ids')
            transactions = []
            # files_name_download = []
            
            for file_id in files_ids:
                file = Document.objects.get(pk=file_id)
                file_name = str(file.docfile).rsplit('.', 1)[0]
                filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
                # print(functions.read_csv(filename))
                transactions = transactions + functions.read_csv(filename)
            # print(transactions)
            
            # combine transactions in one file for easier processing and editing
            df = pd.DataFrame(transactions)
            print(df.head())
            # filename = str(file_name).rsplit('.', 1)[0]
            new_file_path_name = functions.path_and_rename('csv')
            print(new_file_path_name)
            df.to_csv( settings.MEDIA_ROOT + "/"+ new_file_path_name, index=False, header=None)
            
            # save new file name to db
            newdoc = Document(docfile = new_file_path_name)
            newdoc.submitter = request.user
            newdoc.save()
            file_id = newdoc.pk

            print(newdoc.pk)

            file_name_download = '/media/' + new_file_path_name
            file_name = str(new_file_path_name).rsplit('\\', 1)[1]
            print(file_name)
            categories = DictionaryCategories.objects.all()
            return render(request, 'home/missing_categories.html', 
                {
                'transactions': transactions,
                'file_name': file_name,
                'categories': categories,
                'file_id': file_id,
                'file_name_download': file_name_download,
                'bank': bank
                })
        else: # there is no missing category
            print('there is no missing category')
        #     if bank == 'td_csv' or bank == 'atb_csv' or bank == 'rbc_csv' or bank == 'cibc_csv':
        #         file_id = request.POST.get('file_id')
        #         file = Document.objects.get(pk=file_id)
        #         file_name = str(file.docfile).rsplit('.', 1)[0]
        #         filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
        #         transactions = functions.read_csv(filename)
        #         file_name = str(file_name).rsplit('/', 1)[1] + '.csv'
        #         categories = DictionaryCategories.objects.all()
        #         bank = request.POST.get('bank')
        #         # print('bank from categories : ' + str(bank))
        #         return render(request, 'home/categories.html', 
        #                 {
        #                 'categories': categories,
        #                 'transactions': transactions,
        #                 'file_name': file_name,
        #                 'bank': bank
        #                 })
            # else:
            transactions = []
            # files_name_download = []
            print(files_ids)
            for file_id in files_ids:
                file = Document.objects.get(pk=file_id)
                file_name = str(file.docfile).rsplit('.', 1)[0]
                filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
                # print(functions.read_csv(filename))
                transactions = transactions + functions.read_csv(filename)
            # print(transactions)
            
            # combine transactions in one file for easier processing and editing
            df = pd.DataFrame(transactions)
            print(df.head())
            # filename = str(file_name).rsplit('.', 1)[0]
            new_file_path_name = functions.path_and_rename('csv')
            print(new_file_path_name)
            df.to_csv( settings.MEDIA_ROOT + "/"+ new_file_path_name, index=False, header=None)
            
            # save new file name to db
            newdoc = Document(docfile = new_file_path_name)
            newdoc.submitter = request.user
            newdoc.save()
            file_id = newdoc.pk
            
            
            file_name_download = '/media/' + new_file_path_name
            file_name = str(new_file_path_name).rsplit('\\', 1)[1]
            
            return render(request, 'home/download_csv.html', 
                    {
                    'file_name': file_name_download,
                    'file_id': file_id,
                    'bank': bank
                    })
    try:
        return render(request, 'home/download_csv.html')

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# download csv page and go to categories page
@login_required(login_url="/login/")
def categories(request):
    context = {}
    if request.method == "POST":
        print('categories being called')
        file_id = request.POST.get('file_id')
        print(file_id)
        file = Document.objects.get(pk=file_id)
        print(file.docfile)
        # file_name = str(file.docfile).rsplit('.', 1)[0]
        # print(file_name)
        filename = Path(settings.MEDIA_ROOT + str(file.docfile))
        print(filename)
        # print(str(file_name).rsplit('/', 1)[1])
        transactions = functions.read_csv(filename)
        # del transactions[0]
        # sub_categories = DictionarySubcategories.objects.all()
        # categories = []
        # for r in transactions: # for each row in csv file
        #     categories.append(get_category(r[3], sub_categories))
        #     # print(get_sub_category(r[3], sub_categories))
        # # print(categories)
        # zipped_data = zip(transactions, categories)
        # for i, j in zipped_data:
        #     print(str(i[3]) + ' ' + str(j))


        # file_name = str(file_name).rsplit('/', 1)[1] + '.csv'
        categories = DictionaryCategories.objects.all()
        bank = request.POST.get('bank')
        print('bank from categories : ' + str(bank))

        file_name = str(filename).rsplit('\\', 1)[1]
        print(file_name)
        return render(request, 'home/categories.html', 
                {
                'categories': categories,
                'transactions': transactions,
                # 'zipped_data': zipped_data,
                'file_name': file_name,
                'bank': bank
                })


        # print(rows[1])
        # print('categories post called')

    # using try to get the view template
    try:
        # sub_categories = DictionarySubcategories.objects.all()
        # print(get_sub_category('ISLAMIC RELIEF CANADA BURLINGTON', sub_categories))
        # file_path_name = Path(settings.MEDIA_ROOT+ 'statements/' + '138c3b8b9ab944d786ef92ff4697f42b' + '.csv')
        # print(file_path_name)
        # file = open(file_path_name)
        # print(file_path_name)
        # rows = read_csv(file_path_name)
        # print(rows[1])
        return render(request, 'home/categories.html')

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# Upload csv statement page and go to process statement page 
@login_required(login_url="/login/")
def upload_csv_statement(request):
    context = {}
    msg = ''
    current_user = request.user
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            files = request.FILES.getlist('docfile')

            files_ids = []
            bank = request.POST.get('bank')

            for file in files:
                print(file)
                print(file.name.split('.')[-1])
                if file.name.split('.')[-1] == 'csv' or file.name.split('.')[-1] == 'pdf':
                    newdoc = Document(docfile = file)
                    newdoc.submitter = request.user
                    newdoc.save()
                    files_ids.append(newdoc.pk)
                else:
                    msg = 'Unsupported file extension, please upload a .csv or .pdf statement'
                    return render(request, 'home/upload_csv_statement.html',
                                            {'segment': 'upload_csv_statement' ,'form': form, 'msg':msg})
                    

            return render(request, 'home/process_statement.html', 
                {
                'user_id': current_user.id,
                'files_ids': files_ids, 
                'bank': bank
                })
    try:
        form = DocumentCSVForm(request.POST, request.FILES)
        return render(request, 'home/upload_csv_statement.html',{'segment': 'upload_csv_statement' ,'form': form, 'msg':msg})

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# # Upload csv statement page and go to process statement page 
# @login_required(login_url="/login/")
# def upload_statement_multiple(request):
#     context = {}
#     msg = ''
#     current_user = request.user
#     if request.method == "POST":
#         form = DocumentMultipleForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             files = request.FILES.getlist('docfile')

#             file_ids = []
#             for file in files:
#                 print(file)
#                 if file.name.split('.')[-1] != 'csv':
#                     msg = 'Unsupported file extension, please upload a .csv statement'
#                 # newdoc = Document(docfile = file)
#                 # newdoc.submitter = request.user
#                 # newdoc.save()

#                 # file_ids.append(newdoc.pk)
#                 bank = request.POST.get('bank')

#             for x in file_ids:
#                 print(x)
#         # print(request.FILES)
#         # if request.FILES['docfile'].name.split('.')[-1] != 'csv':
#         #     # print('error pfd')
#         #     msg = 'Unsupported file extension, please upload a .csv statement'
#         # else:
#         # newdoc = Document(docfile = request.FILES['docfile'])
#         # newdoc.submitter = request.user
#         # # print(newdoc)
#         # newdoc.save()
#         # print(newdoc.docfile)
#         # return render(request, 'home/process_multiple_statement.html', 
#         #     {
#         #     'user_id': current_user.id,
#         #     'file_ids': file_ids, 
#         #     'bank': bank
#         #     })
#     try:
#         form = DocumentMultipleForm(request.POST, request.FILES)
#         return render(request, 'home/upload_statement_multiple.html',{'segment': 'upload_multiple_statement' ,'form': form, 'msg':msg})

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))
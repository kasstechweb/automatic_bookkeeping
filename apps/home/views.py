# -*- encoding: utf-8 -*-

from pathlib import Path
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings

from .models import DictionaryCategories, DictionarySubcategories, Document, Company

# from django.shortcuts import render  
from .forms import DocumentForm, DocumentCSVForm, DocumentMultipleForm
from django.shortcuts import render
from apps.home import functions, path_rename
import ast
import pandas as pd
import os
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

# Upload csv statement page and go to process statement page 
@login_required(login_url="/login/")
def upload_statement(request):
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
                if file.name.split('.')[-1] == 'csv' or file.name.split('.')[-1] == 'pdf':
                    newdoc = Document(docfile = file)
                    newdoc.submitter = request.user
                    newdoc.save()
                    files_ids.append(newdoc.pk)
                else:
                    msg = 'Unsupported file extension, please upload a .csv or .pdf statement'
                    return render(request, 'home/upload_statement.html',
                                            {'segment': 'upload_csv_statement' ,'form': form, 'msg':msg})
                    

            return render(request, 'home/process_statement.html', 
                {
                'user_id': current_user.id,
                'files_ids': files_ids, 
                'bank': bank
                })
    try:
        form = DocumentCSVForm(request.POST, request.FILES)
        return render(request, 'home/upload_statement.html',{'segment': 'upload_statement' ,'form': form, 'msg':msg})

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
    try:
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

        # if missing category already done skip
        missing_categories = request.POST.get('missing_categories')
        # check banks
        bank = request.POST.get('bank')
        if missing_categories == 'skip':
            file_id = request.POST.get('file_id')
            db_row = Document.objects.get(pk=file_id)
            file_name = db_row.docfile

            file_name_download = '/media/' + str(file_name)
            
            return render(request, 'home/download_csv.html', 
                    {
                    'file_name': file_name_download,
                    'file_id': file_id,
                    'bank': bank
                        })
        else:
            files_ids = request.POST.get('files_ids')
            files_ids = ast.literal_eval(files_ids)
            
            missing_category_list = []
            for file_id in files_ids:
                # print(file_id)
                file = Document.objects.get(pk=file_id)
                file_name = file.docfile
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
                    elif bank == 'scotia':
                        check_missing_category = functions.scotia_process_csv(file_name)
                        missing_category_list.append(check_missing_category)
            
            if True in missing_category_list: # there is a missing category ask user to add it before downloading csv
                transactions = []
                
                for file_id in files_ids:
                    print(file_id)
                    file = Document.objects.get(pk=file_id)
                    file_name = str(file.docfile).rsplit('.', 1)[0]
                    filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
                    transactions = transactions + functions.read_csv(filename)
                    # remove the csv file after adding it to new combining file
                    # os.remove(filename)
                
                # combine transactions in one file for easier processing and editing
                df = pd.DataFrame(transactions)
                new_file_path_name = functions.path_and_rename('csv')
                df.to_csv( settings.MEDIA_ROOT + "/"+ new_file_path_name, index=False, header=None)
                
                # save new file name to db
                newdoc = Document(docfile = new_file_path_name)
                newdoc.submitter = request.user
                newdoc.save()
                new_file_id = newdoc.pk

                file_name_download = '/media/' + new_file_path_name
                file_name = str(new_file_path_name).rsplit('\\', 1)[1]
                categories = DictionaryCategories.objects.all()

                # delete files and from db
                for file_id in files_ids:
                    file = Document.objects.get(pk=file_id)
                    file_path_name = file.docfile
                    os.remove(Path(settings.MEDIA_ROOT + str(file_path_name)))
                    file_no_ext = str(file.docfile).rsplit('.', 1)[0]
                    file_name_csv = file_no_ext + '.csv'
                    os.remove(Path(settings.MEDIA_ROOT + str(file_name_csv)))
                    Document.objects.filter(pk=file_id).delete()

                return render(request, 'home/missing_categories.html', 
                    {
                    'transactions': transactions,
                    'file_name': file_name,
                    'categories': categories,
                    'file_id': new_file_id,
                    'file_name_download': file_name_download,
                    'bank': bank
                    })
            else: # there is no missing category
                transactions = []
                for file_id in files_ids:
                    file = Document.objects.get(pk=file_id)
                    file_name = str(file.docfile).rsplit('.', 1)[0]
                    filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
                    transactions = transactions + functions.read_csv(filename)
                    # remove the csv file after adding it to new combining file
                    # os.remove(filename)
                
                # combine transactions in one file for easier processing and editing
                df = pd.DataFrame(transactions)
                new_file_path_name = functions.path_and_rename('csv')
                df.to_csv( settings.MEDIA_ROOT + "/"+ new_file_path_name, index=False, header=None)
                
                # save new file name to db
                newdoc = Document(docfile = new_file_path_name)
                newdoc.submitter = request.user
                newdoc.save()
                new_file_id = newdoc.pk
                
                file_name_download = '/media/' + new_file_path_name
                file_name = str(new_file_path_name).rsplit('\\', 1)[1]
                
                # delete files and from db
                for file_id in files_ids:
                    file = Document.objects.get(pk=file_id)
                    file_path_name = file.docfile
                    os.remove(Path(settings.MEDIA_ROOT + str(file_path_name)))
                    file_no_ext = str(file.docfile).rsplit('.', 1)[0]
                    file_name_csv = file_no_ext + '.csv'
                    os.remove(Path(settings.MEDIA_ROOT + str(file_name_csv)))
                    Document.objects.filter(pk=file_id).delete()

                return render(request, 'home/download_csv.html', 
                        {
                        'file_name': file_name_download,
                        'file_id': new_file_id,
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
        file_id = request.POST.get('file_id')
        
        file = Document.objects.get(pk=file_id)
        filename = Path(settings.MEDIA_ROOT + str(file.docfile))
        transactions = functions.read_csv(filename)
        categories = DictionaryCategories.objects.all()
        bank = request.POST.get('bank')

        file_name = str(filename).rsplit('\\', 1)[1]
        file_download = '/media/statements/' + file_name
        return render(request, 'home/categories.html', 
                {
                'categories': categories,
                'transactions': transactions,
                # 'zipped_data': zipped_data,
                'file_name': file_name,
                'file_download': file_download,
                'bank': bank
                })
    # using try to get the view template
    try:
        return render(request, 'home/categories.html')

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# statements_history
@login_required(login_url="/login/")
def statements_history(request):
    context = {}
    try:
        documents = Document.objects.filter( submitter_id = request.user)
        for document in documents:
            document.docfile = str(document.docfile).rsplit('\\', 1)[1]
            # print(document.docfile)
            # print(document.date)
        return render(request, 'home/statements_history.html',
                                {
                                    'segment': 'statements_history',
                                    'documents': documents
                                })

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# categories_summary
@login_required(login_url="/login/")
def categories_summary(request):
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        print(file_name)
        transactions = functions.read_csv(Path(settings.MEDIA_ROOT + '/statements/' + file_name) )
        categories = DictionaryCategories.objects.all()
        summary = []

        current_user = request.user
        print(current_user.id)
        company_details = Company.objects.get(user_id = current_user.id)
        # for tr in transactions:
        #     print(tr)

        for cat in categories:
            duplicates = []
            for index,tr in enumerate(transactions):
                # print(tr)
                if cat.name == tr[5]:
                    duplicates.append(index)
            
            withdrawn = 0.00
            deposited = 0.00
            # itterate and gather withdrawn and deposited for each category
            for dup in duplicates:
                # print(transactions[dup][2])
                if transactions[dup][2] != '':
                    amount = functions.clean_amount(transactions[dup][2])
                    withdrawn += float(amount)
                if transactions[dup][3] != '':
                    amount = functions.clean_amount(transactions[dup][3])
                    deposited += float(amount)
            # add category name and total amount to summary 
            if withdrawn != 0.00 or deposited != 0.00:
                summary.append([cat.name, format(withdrawn, '.2f'), format(deposited, '.2f')])
        
        new_filename = str(file_name).rsplit('.', 1)[0]

        # percentage file logic
        percentage_file = Path(settings.MEDIA_ROOT + '/statements/' + new_filename +  str('_percent.txt'))
        if not os.path.exists(percentage_file):
            for index, x in enumerate(summary):
                # print(index+1)
                functions.categories_percent_write(new_filename, index+1, 100)
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

        # for x in summary:
        #     print(x)

        gfi_file = '/media/statements/' + new_filename + ".gfi"
        # functions.categories_percent_read(new_filename)
        # functions.categories_percent_write(new_filename, 2, 57)
        # functions.categories_percent_write(new_filename, 5, 57)
        return render(request, 'home/categories_summary.html',
                                {
                                    'summary': summary,
                                    'company_details': company_details,
                                    'gfi_file': gfi_file,
                                    'new_filename': new_filename,
                                })

    # try:
    #     # documents = Document.objects.filter( submitter_id = request.user)
    #     # for document in documents:
    #     #     document.docfile = str(document.docfile).rsplit('\\', 1)[1]
    #     #     print(document.docfile)
    #     #     print(document.date)
    #     return render(request, 'home/categories_summary.html',
    #                             {
    #                                 'segment': 'categories_summary',
    #                             })

    # except template.TemplateDoesNotExist:
    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))


# process statement page and go to download page 
@login_required(login_url="/login/")
def profile(request):
    context = {}
    current_user = request.user
    if Company.objects.filter(user_id = current_user.id).exists():
        user_company = Company.objects.get(user_id = current_user.id)
    else:
        user_company = ''
    print(user_company)
    if user_company.name == None:
        user_company.name = ''
    if user_company.phone == None:
        user_company.phone = ''
    if user_company.street == None:
        user_company.street = ''
    if user_company.city == None:
        user_company.city = ''
    if user_company.province == None:
        user_company.province = ''
    if user_company.zip == None:
        user_company.zip = ''
    print(user_company.street)
    try:
        return render(request, 'home/profile.html', 
            {
                'segment': 'profile',
                'current_user': current_user,
                'user_company': user_company
            })

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

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
from .forms import DocumentForm, DocumentCSVForm
from django.shortcuts import render
from apps.home import functions
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
    if request.method == "POST":
        print('process statement post called')
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
        # print('download_csv post called')
        file_id = request.POST.get('file_id')
        file = Document.objects.get(pk=file_id)
        file_name = file.docfile

        # check banks
        bank = request.POST.get('bank')
        print('bank is : ' + bank)
        if bank == 'td':
            check_missing_category = functions.td_pdftocsv(request, file_name)
        elif bank == 'rbc':
            check_missing_category = functions.rbc_pdftocsv(request, file_name)
        elif bank == 'atb':
            check_missing_category = functions.atb_pdftocsv(request, file_name)
        elif bank == 'servus':
            check_missing_category = functions.servus_pdftocsv(request, file_name)
        elif bank == 'scotia':
            check_missing_category = functions.scotia_pdftocsv(request, file_name)
        elif bank == 'td_csv':
            check_missing_category = functions.td_process_csv(file_name)
        elif bank == 'atb_csv':
            check_missing_category = functions.atb_process_csv(file_name)
        elif bank == 'rbc_csv':
            check_missing_category = functions.rbc_process_csv(file_name)
        
        if check_missing_category == True: # there is a missing category ask user to add it before downloading csv
            print('there is missing category')
            file_id = request.POST.get('file_id')
            file = Document.objects.get(pk=file_id)
            file_name = str(file.docfile).rsplit('.', 1)[0]
            filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
            # print(file_name)
            # print(str(file_name).rsplit('/', 1)[1])
            transactions = functions.read_csv(filename)
            file_name = str(file_name).rsplit('/', 1)[1] + '.csv'
            file_name_download = '/media/statements/' + file_name
            # del transactions[0]
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
            filename = str(file_name).rsplit('.', 1)[0]
            filename = '/media/' + filename + '.csv'
            
            return render(request, 'home/download_csv.html', 
                    {
                    'file_name': filename,
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
        file_id = request.POST.get('file_id')
        file = Document.objects.get(pk=file_id)
        file_name = str(file.docfile).rsplit('.', 1)[0]
        filename = Path(settings.MEDIA_ROOT + file_name + '.csv')
        # print(file_name)
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
        file_name = str(file_name).rsplit('/', 1)[1] + '.csv'
        categories = DictionaryCategories.objects.all()
        bank = request.POST.get('bank')
        print('bank from categories : ' + str(bank))
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
            # print(request.POST.get('bank'))
            bank = request.POST.get('bank')
            # print(request.FILES)
            if request.FILES['docfile'].name.split('.')[-1] != 'csv':
                # print('error pfd')
                msg = 'Unsupported file extension, please upload a .csv statement'
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
    try:
        form = DocumentCSVForm(request.POST, request.FILES)
        return render(request, 'home/upload_csv_statement.html',{'segment': 'upload_csv_statement' ,'form': form, 'msg':msg})

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


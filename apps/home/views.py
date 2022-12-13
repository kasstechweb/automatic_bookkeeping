# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings

from .models import Document

# from django.shortcuts import render  
from .forms import DocumentForm
from django.shortcuts import render
from .functions import td_pdftocsv, get_categories


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
    context = {}
    msg = ''
    current_user = request.user
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            # print(request.POST.get('bank'))
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
                    'file_id': newdoc.pk
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
        return render(request, 'home/upload_statement.html',{'form': form, 'msg':msg})

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
        file_id = request.POST.get('file_id')
        file = Document.objects.get(pk=file_id)
        file_name = file.docfile
        td_pdftocsv(request, file_name)
        filename = str(file_name).rsplit('.', 1)[0]
        filename = settings.MEDIA_ROOT + filename + '.csv'
        return render(request, 'home/download_csv.html', 
                {
                'file_name': filename
                })
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
    try:
        get_categories(request, '')
        return render(request, 'home/categories.html')

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
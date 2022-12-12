# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Document

# from django.shortcuts import render  
from .forms import DocumentForm
from django.shortcuts import render
from .functions import handle_uploaded_file


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

# Upload statement page and post 
@login_required(login_url="/login/")
def upload_statement(request):
    context = {}
    msg = ''
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            print(request.POST.get('bank'))
            print(request.FILES)
            if request.FILES['docfile'].name.split('.')[-1] != 'pdf':
                # print('error pfd')
                msg = 'Unsupported file extension, please upload a .pdf statement'
            else:
                newdoc = Document(docfile = request.FILES['docfile'])
                newdoc.save()
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

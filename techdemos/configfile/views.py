from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings

from .forms import UploadFileForm
from .bngl import interpret_bngl, make_config


import os

# Create your views here.

file = ""
config_str = ""

def index(request):    
    if request.method == 'POST':
        global file
        file = handle_uploaded_file(request.FILES['myfile'])
        return redirect('create.html')

    return render(request, 'configfile/home.html')

def create(request):
    if request.method == 'POST':
        global config_str
        config_str = make_config(request.POST)
        return redirect('config.html')
    else:
        global file
        content_dict = interpret_bngl(file)
        return render(request, 'configfile/create.html', content_dict)

def config(request):
    global config_str
    print(config_str)
    return render(request, 'configfile/config.html', {'content': config_str})

def handle_uploaded_file(f):
    out = os.path.join(settings.MEDIA_ROOT, 'user_input.bngl')
    with open('user_input.bngl', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return 'C:\\Users\\Josh\\Desktop\\BioNetWeb\\techdemos\\user_input.bngl'


from django.shortcuts import render
from django.http import HttpResponse
from .models import fileform,PlikDoPobrania,plik
from .functions import readtxt
from django.conf import settings
from django.shortcuts import Http404
import os
# Create your views here.
def kasa(request, *args, **kwargs):
    url='kasa/kasa.html'
    context = {
    }

    if request.method == 'POST':
        myform = fileform(request.POST, request.FILES)
        if myform.is_valid():
            myplik = plik()
            myplik.description = myform.cleaned_data["description"]
            myplik.path = myform.cleaned_data["path"]
            print(myplik.path,myplik.description)
            myplik.save()
            kasa = readtxt(myplik)
            #intr = xls2intr(myplik)
    else:
        myform=fileform()
    myPlikDoPobrania = PlikDoPobrania()
    myPlikDoPobrania.save()
    return render(request,url,locals())




    return HttpResponse("222")
def download(request,path='apps/kasa/out.txt'):

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        print(file_path)
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


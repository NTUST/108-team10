from django.shortcuts import render
from django.http import *
import datetime as d

def hello(request):
    dd = d.datetime.now()
    #return HttpResponse('<h1>Hello World!</h1>')
    return render(request,'test_index.html',{'time':dd})
# Create your views here.

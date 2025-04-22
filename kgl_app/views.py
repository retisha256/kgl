from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):

        
    
        
    return render(request, 'index.html')

def dash(request):
    return render (request, 'dash.html')

def addstock(request):
    return render(request, 'addstock.html')

def addsales(request):

    return render(request, 'addsales.html')

def receipt(request):
    return render (request,'receipt.html')

def allstock(request):
    stocks=Stock.objects.all().order_by('-id')
    return render (request,'allstock.html',{'stocks':stocks})

def allsales(request):
    sales=Sales.objects.all().order_by('-id')
    return render (request,'allsales.html',{'sales':sales})

def addcredit(request):
    return render (request, 'addcredit')

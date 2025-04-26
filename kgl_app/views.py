from django.shortcuts import render, redirect
#accessing  all our models 
from .models import *
from django.urls import reverse
from .forms import *
#borrowing decorators from django to restrict our views
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import AuthenticationForm 


# Create your views here.
#view for indexpage

def Login(request):
    if request.method =="POST":
        username =request.POST['username']
        password = request.POST['password']
        user =authenticate(request, username = username,password=password)
        if user is not None and user.is_owner==True:
            form =login(request,user)
            return redirect('/dashboard3')
        
        if user is not None and user.is_manager==True:
            form =login(request,user)
            return redirect('/dashboard1')
        
        if user is not None and user.is_salesagent==True:
            form =login(request,user)
            return redirect('/dashboard2')
        else:
            print("Sorry!, something went wrong")
    form = AuthenticationForm()
    return render(request, 'login.html',{"form":form})

def signup(request):
    if request.method=="POST":
        form =UserCreation(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return redirect('/login')
    else:
            form =UserCreation()
    return render (request, 'signup.html',{'form':form})

    
   
def dash(request):
    return render (request, 'dash.html')

#view for receiptpage

def receipt(request):
    sales = Sales.objects.all().order_by("-id")
    return render(request, "receipt.html",{'sales':sales})

#view for addsales

def addsales(request):
    return render(request, "addsales.html")

#view for addstock

def addstock(request,pk):
    issued_item =Stock.objects.get(id=pk)
    form=UpdateStockForm(request.POST)

    if request.method =="POST":
        if form.is_valid():
            added_quantity=int(request.POST['received_quantity'])
            issued_item.total_quantity += added_quantity
            issued_item.save()
          #to add to the remaining stock quantity is increasing
            print(added_quantity)
            print(issued_item.total_quantity)
            return redirect('index')
    return render(request, "addstock.html", {'form':form})

#view all sales
def allsales(request):
    sales =Sales.objects.all().order_by('-id')
    return render(request, "allsales.html",{'sales':sales})

#view all stock

def allstock(request):
    stocks =Stock.objects.all().order_by('-id')
    return render(request, "allstock.html",{'stocks':stocks})

#view to handle a link for a particular item to sell an item

def  detail(request, stock_id):
    stock =Stock.objects.get(id=stock_id)
    return render(request,'stock_detail.html' ,{'stock':stock})

def issue_item(request,pk):
    #creating a variable issued item and access all entries in the stock model by their id
    issued_item= Stock.objects.get(id=pk)
    #accessing our form from forms.py
    sales_form =AddSalesForm(request.POST)
    
    if request.method== 'POST':

        if sales_form.is_valid():
            new_sale =sales_form.save(commit = False)
            new_sale.item_name = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()
            #To keep track of the stock after sales
            issued_quantity =int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save()
            print(issued_item.item_name)
            print(request.POST['quantity'])
            print(issued_item.total_quantity)

            return redirect('receipt')
    return render(request,'issue_item.html',{'sales_form':sales_form}) 
       
def receipt_detail(request,receipt_id):
    receipt= Sales.objects.get(id=receipt_id)
    return render (request,  'receipt_detail.html', {'receipt':receipt})
def addcredit(request):
    return render(request,'addcredit')
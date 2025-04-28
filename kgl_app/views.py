from django.shortcuts import render, redirect, get_object_or_404
#accessing  all our models 
from .models import *
from django.urls import reverse
from .forms import *
#borrowing decorators from django to restrict our views
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.db.models import Sum, Count # Import aggregate functions
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
#view for indexpage

def Login(request):
    if request.method =="POST":
        username =request.POST['username']
        password = request.POST['password']
        user =authenticate(request, username = username,password=password)
        if user is not None and user.is_owner==True:
            form =login(request,user)
            return redirect('/dashboard2/')
        
        if user is not None and user.is_manager==True:
            form =login(request,user)
            return redirect('/dash2/')
        
        if user is not None and user.is_salesagent==True:
            form =login(request,user)
            return redirect('/dash1/')
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
def is_manager_check(user):
    return user.is_manager

@login_required
@user_passes_test(is_manager_check)
def addstock(request,pk):
    issued_item =Stock.objects.get(id=pk)
    form=UpdateStockForm(request.POST)

    if request.method =="POST":
        if form.is_valid():
            added_quantity=int(request.POST['received_quantity'])
            issued_item.tonnage += added_quantity
            issued_item.save()
          #to add to the remaining stock quantity is increasing
            print(added_quantity)
            print(issued_item.tonnage)
            return redirect('allstock')
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
    return render(request,'detail.html' ,{'stock':stock})

def delete_stock(request, stock_id):
    stock =Stock.objects.get(id=stock_id) # Get the Sale object or show 404 if not found
    if request.method == 'POST':  # Ensure it's a POST request (safer for deleting)
        stock.delete()
        return redirect('allstock')  # Redirect to your sales list view
    #  Add this else block
    else:
        return render(request, 'stock_confirm_delete.html', {'stock': stock}) 


def issue_item(request,pk):
    #creating a variable issued item and access all entries in the stock model by their id
    issued_item= Stock.objects.get(id=pk)
    #accessing our form from forms.py
    sales_form =AddSalesForm(request.POST)
    
    if request.method== 'POST':

        if sales_form.is_valid():
            new_sale =sales_form.save(commit = False)
            new_sale.name_of_produce = issued_item
            new_sale.selling_price = issued_item.selling_price
            new_sale.save()
            #To keep track of the stock after sales
            issued_quantity =int(request.POST['tonnage'])
            issued_item.tonnage -= issued_quantity
            issued_item.save()
            print(issued_item.name_of_produce)
            print(request.POST['tonnage'])
            print(issued_item.tonnage)

            return redirect('receipt')
    return render(request,'issue_item.html',{'sales_form':sales_form}) 


       
def receipt_detail(request,receipt_id):
    receipt= Sales.objects.get(id=receipt_id)
    return render (request,  'receipt_detail.html', {'receipt':receipt})
def addcredit(request):
    credit=Credit.objects.all().order_by("-id")
    return render(request,'addcredit.html',{'credit':credit})
def manager(request):
    return render (request,"dash2.html" )


#view for the owner
def owner(request):
    
    return render(request, 'dash1.html') 
   
#view for salesagent
def salesagent(request):
    return render (request,'dashboard2.html')

def Logout(request):
    return render(request,'logout.html' )

def delete_sale(request, sale_id):
    sale =Sales.objects.get(id=sale_id) # Get the Sale object or show 404 if not found
    if request.method == 'POST':  # Ensure it's a POST request (safer for deleting)
        sale.delete()
        return redirect('allsales')  # Redirect to your sales list view
    #  Add this else block
    else:
        return render(request, 'sale_confirm_delete.html', {'sale': sale}) 

def view_sale(request, sale_id):
    sale =Sales.objects.get(id=sale_id)  # Get the Sale object or show 404 if not found
    context = {'sale': sale}  # Pass the Sale object to the template
    return render(request, 'sale_detail.html', context)  # Render the template

def branch_sales(request, branch_name): # Change the view name and add branch_name parameter
    """
    Displays all sales for a specific branch.
    """
    sales = Sales.objects.filter(branch=branch_name) # Filter sales by branch name

    context = {
        'sales': sales,
        'branch_name': branch_name,  # Pass the branch name to the template
    }
    return render(request, 'branch_sales.html', context) 

def sales_report(request):
    """
    Generates a sales report.
    """
    all_sales = Sales.objects.all()  # Get all sales records

    total_sales_amount = 0  # Initialize total sales
    for sale in all_sales:
        total_sales_amount += sale.total_sales()  # Call the method for each sale

    total_sales_count = all_sales.count()
    average_sale_amount = total_sales_amount / total_sales_count if total_sales_count else 0

    context = {
        'total_sales_amount': total_sales_amount,
        'total_sales_count': total_sales_count,
        'average_sale_amount': average_sale_amount,
        'all_sales': all_sales,
    }
    return render(request, 'sales_report.html', context)




def notify_managers(product_name):
    """
    Sends an email notification to all managers about a stockout.
    """
    managers = Userprofile.objects.filter(is_manager=True)
    manager_emails = [manager.email for manager in managers if manager.email]  # Get emails

    if manager_emails:  # Only send if there are managers with emails
        subject = f"Stock Out of Stock: {product_name}"
        message = f"The product '{product_name}' is out of stock."
        from_email = settings.DEFAULT_FROM_EMAIL  # Use your default email setting
        send_mail(subject, message, from_email, manager_emails)

def create_sale(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        tonnage = int(request.POST.get('tonnage'))
        #  Get the stock object
        stock = get_object_or_404(Stock, pk=product_id)

        # Check if there is enough stock
        if stock.current_stock >= tonnage:
            # Use a transaction to ensure atomicity (all or nothing)
            with transaction.atomic():
                # Update stock:  IMPORTANT - Do this *before* creating the sale
                stock.current_stock -= tonnage
                stock.save()  # Save the updated stock

                # Create the sale
                sale = Sales(
                    product_name=stock,  # Use the stock object
                    tonnage=tonnage,
                    amount_paid=int(request.POST.get('amount_paid')),
                    buyers_name=request.POST.get('buyers_name'),
                    salesagent_name=request.user,  # Use request.user
                    is_sold_on_cash=request.POST.get('is_sold_on_cash') == 'True',
                    branch=stock.branch,  # Get branch from the stock
                    selling_price=stock.selling_price
                )
                sale.save()

            messages.success(request, "Sale recorded successfully.")
            return redirect('all_sales')  # Redirect to sales list

        else:
            messages.error(request, f"Not enough stock. Only {stock.current_stock} available.")
            # Notify managers (asynchronously if possible - see below)
            notify_managers(stock.name_of_produce)
            return redirect('create_sale')  # Or back to the form

    # Handle GET request (display the form)
    stocks = Stock.objects.filter(current_stock__gt=0)  # Only show in-stock products
    return render(request, 'create_sale.html', {'stocks': stocks})
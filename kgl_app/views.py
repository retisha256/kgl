from django.shortcuts import render, redirect, get_object_or_404
# accessing  all our models
from .models import *
from django.urls import reverse
from .forms import *
# borrowing decorators from django to restrict our views
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count  # Import aggregate functions
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Sum, Q


# Create your views here.
# view for indexpage

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def Login(request):
    """
    Handles user login based on their role (owner, manager, sales agent).
    Redirects to the appropriate dashboard upon successful authentication.
    Displays an error message if authentication fails.
    """
    error_message = None  # Initialize an error message variable

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_owner:
                login(request, user)
                return redirect('/dashboard2/')
            elif user.is_manager:
                login(request, user)
                return redirect('/dash2/')
            elif user.is_salesagent:
                login(request, user)
                return redirect('/dash1/')
            else:
                error_message = "Your account doesn't have a defined role."
        else:
            error_message = "Invalid username or password."

    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form, "error_message": error_message})

def is_owner_check(user):
    """
    Checks if the given user has owner status.
    """
    return user.is_owner

# Define a function to check for manager status
def is_manager_check(user):
    """
    Checks if the given user has manager status.
    """
    return user.is_manager

# Define a function to check for sales agent status
def is_salesagent_check(user):
    """
    Checks if the given user has sales agent status.
    """
    return user.is_salesagent

@login_required
@user_passes_test(is_manager_check)
def signup(request):
    """
    Handles user registration. Creates a new user upon successful form submission
    and redirects them to the login page.
    """
    if request.method == "POST":
        form = SalesAgentSignUpForm(request.POST)  # Use the new form
        if form.is_valid():
            user = form.save()  # Save the user
            user.is_salesagent = True  # Set the user as a sales agent
            user.save()
            login(request, user)
            return redirect('/login')
    else:
        form = SalesAgentSignUpForm()  # Use the new form
    return render(request, 'signup.html', {'form': form})
    # Define a function to check for owner status


def index(request):
    """
    Renders a generic dashboard page.
    """
    return render(request, 'dashboard_default.html')

# view for receiptpage


@user_passes_test(is_manager_check or is_salesagent_check)
def receipt(request):
    """
    Displays a list of all sales receipts, ordered by the most recent.
    """
    sales = Sales.objects.all().order_by("-id")
    return render(request, "receipt.html", {'sales': sales})

# view for addsales

@user_passes_test(is_manager_check or is_salesagent_check)
def addsales(request):
    """
    Renders the page for adding new sales (this view might not be directly used
    as the 'issue_item' view handles the creation of sales records).
    """
    return render(request, "addsales.html")

# view all sales
def allsales(request):
    """
    Displays a list of all sales records, ordered by the most recent.

    """
    if request.user.is_manager or request.user.is_salesagent:
     sales =Sales.objects.filter(branch=request.user.branch)
    else:
     sales = Sales.objects.all().order_by('-id')
    return render(request, "allsales.html", {'sales': sales})


@user_passes_test(is_manager_check or is_salesagent_check)
def issue_item(request, pk):
    """
    Handles the process of issuing an item (creating a sale record).
    Retrieves the stock item based on the provided primary key (pk).
    If the request method is POST, it processes the AddSalesForm,
    creates a new sale record linked to the issued stock item,
    updates the stock quantity, and redirects to the receipt page.
    """
    # creating a variable issued item and access all entries in the stock model by their id
    issued_item = get_object_or_404(Stock, id=pk)
    # accessing our form from forms.py
    sales_form = AddSalesForm(request.POST)

    if request.method == 'POST':
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.name_of_produce = issued_item
            new_sale.selling_price = issued_item.selling_price
            new_sale.branch = issued_item.branch  # Assign the branch from the stock item
            new_sale.salesagent_name = request.user  # Assign the logged-in user as the sales agent
            new_sale.save()
            # To keep track of the stock after sales
            issued_quantity = int(request.POST['tonnage'])
            issued_item.tonnage -= issued_quantity
            issued_item.save()
            print(issued_item.name_of_produce)
            print(request.POST['tonnage'])
            print(issued_item.tonnage)

            return redirect('receipt')
    return render(request, 'issue_item.html', {'sales_form': sales_form})

@user_passes_test(is_manager_check or is_salesagent_check)

def receipt_detail(request, receipt_id):
    """
    Displays the details of a specific sales receipt based on the provided receipt ID.
    """
    receipt = get_object_or_404(Sales, id=receipt_id)
    return render(request, 'receipt_detail.html', {'receipt': receipt})

# view all stock
#Displays a list of all stock items, ordered by the most recent.
def allstock(request):
    if request.user.is_manager or request.user.is_salesagent:
     stocks =Stock.objects.filter(branch=request.user.branch)
    else:
     stocks = Stock.objects.all().order_by('-id')
    return render(request, "allstock.html", {'stocks': stocks})

# view to handle a link for a particular item to sell an item
#Displays the details of a specific stock item based on the provided stock ID.
def detail(request, stock_id):
   
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'detail.html', {'stock': stock})

# view for deleting stock

@user_passes_test(is_manager_check)
# Handles the deletion of a specific stock item.
def delete_stock(request, stock_id):
    """
   
    It retrieves the stock item based on the provided stock ID.
    If the request method is POST, it deletes the stock item and redirects to the all stock page.
    Otherwise, it renders a confirmation page for deleting the stock.
    """
    stock = get_object_or_404(Stock, id=stock_id)  # Get the Sale object or show 404 if not found
    if request.method == 'POST':  # Ensure it's a POST request (safer for deleting)
        stock.delete()
        return redirect('allstock')  # Redirect to your sales list view
    #   Add this else block
    else:
        return render(request, 'stock_confirm_delete.html', {'stock': stock})


@user_passes_test(is_manager_check)
# view for addingstock
def addstock(request, pk):
    """
    Allows a manager to add more quantity to an existing stock item.
    It retrieves the stock item based on the provided primary key (pk).
    If the request method is POST and the form is valid, it updates
    the stock quantity and redirects to the all stock page.
    """
    issued_item = get_object_or_404(Stock, id=pk)
    form = UpdateStockForm(request.POST, instance=issued_item)  # Initialize form with instance

    if request.method == "POST":
        if form.is_valid():
            form.save()  # Save the changes to the existing instance
            added_quantity = int(request.POST['received_quantity'])
            issued_item.tonnage += added_quantity
            issued_item.save()
            # to add to the remaining stock quantity is increasing
            print(added_quantity)
            print(issued_item.tonnage)
            return redirect('allstock')
    else:
        form = UpdateStockForm(instance=issued_item)  # Populate form with current data
    return render(request, "addstock.html", {'form': form, 'stock_item': issued_item})

# view for addcredit

def addcredit(request):
    """Displays the list of credit entries."""
    credit = Credit.objects.all().order_by("-Dispatch_date")
    return render(request, 'addcredit.html', {'credit': credit}) # Assuming your template is named addcredit.html

def add_credit(request):
    """Handles the creation of a new credit entry."""
    if request.method == 'POST':
        form = AddCreditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addcredit')
    else:
        form = AddCreditForm()
    return render(request, 'add_credit_form.html', {'form': form}) # Create this template

@user_passes_test(is_manager_check )
def delete_credit_list(request):
    """Displays a list of credit entries with checkboxes for deletion."""
    credit = Credit.objects.all().order_by("-Dispatch_date")
    return render(request, 'delete_credit_list.html', {'credit': credit}) # Create this template

@user_passes_test(is_manager_check or is_salesagent_check)
def delete_credit(request, credit_id):
    """Deletes a specific credit entry."""
    credit = get_object_or_404(Credit, id=credit_id)
    if request.method == 'POST':
        credit.delete()
        return redirect('delete_credit_list')
    return render(request, 'delete_credit_confirm.html', {'credit': credit}) 





def delete_sale(request, sale_id):
    """
    Handles the deletion of a specific sale record.
    It retrieves the sale record based on the provided sale ID.
    If the request method is POST, it deletes the sale record and redirects to the all sales page.
    Otherwise, it renders a confirmation page for deleting the sale.
    """
    sale = get_object_or_404(Sales, id=sale_id)  # Get the Sale object or show 404 if not found
    if request.method == 'POST':  # Ensure it's a POST request (safer for deleting)
        sale.delete()
        return redirect('allsales')  # Redirect to your sales list view
    #   Add this else block
    else:
        return render(request, 'sale_confirm_delete.html', {'sale': sale})
    
@user_passes_test(is_manager_check or is_salesagent_check)
def view_sale(request, sale_id):
    """
    Displays the details of a specific sale record based on the provided sale ID.
    """
    sale = get_object_or_404(Sales, id=sale_id)  # Get the Sale object or show 404 if not found
    context = {'sale': sale}  # Pass the Sale object to the template
    return render(request, 'sale_detail.html', context)  # Render the template

@user_passes_test(is_manager_check or is_salesagent_check)
def edit_sale(request, sale_id):
    """
    Allows editing of an existing sale record.
    It retrieves the sale record based on the provided sale ID.
    If the request method is POST, it populates the AddSalesForm with the POST data
    and the existing sale instance, saves the updated sale, and redirects to the all sales page.
    Otherwise, it populates the form with the current data of the sale for editing.
    """
    sale = get_object_or_404(Sales, id=sale_id)  # Get the sale object to edit

    if request.method == 'POST':
        # Populate the form with the POST data, including the instance to update
        form = AddSalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()  # Save the updated sale
            return redirect('allsales')  # Redirect to the list of all sales
    else:
        # Populate the form with the sale's current data for editing
        form = AddSalesForm(instance=sale)

    context = {
        'form': form,
        'sale_id': sale_id,  # Pass the sale_id to the template, if needed
    }
    return render(request, 'edit_sale.html', context)

@user_passes_test(is_manager_check or is_salesagent_check)
def addsale(request):
    if request.method == 'POST':
        form = AddSalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('allsales'))  # Redirect to the all sales page
    else:
        form =AddSalesForm()
    return render(request, 'addsales.html', {'form': form})

 # Import your models

def manager(request):
    total_cash_sales=Sales.objects.filter(is_sold_on_cash=True).aggregate( 
        total_cash=Sum('amount_paid')
    )['total_cash'] or 0
    total_credit_sales=Credit.objects.aggregate(
        total_credit=Sum('amount_due')
    )['total_credit'] or 0
    total_sales=total_cash_sales + total_credit_sales
    total_stock=Stock.objects.aggregate(
        total_quantity=Sum('tonnage')
    )['total_quantity'] or 0
    low_stock_items =Stock.objects.filter(current_stock__lt=10)
    context ={
        'total_cash_sales': total_cash_sales,
        'total_credit_sales': total_credit_sales,
        'total_sales': total_sales,
        'total_stock': total_stock,
        'low_stock_items':low_stock_items,
    }
    return render(request, 'dash2.html', context)

def owner(request):
  total_cash_sales=Sales.objects.filter(is_sold_on_cash=True).aggregate(
    total_cash=Sum('amount_paid')
  )['total_cash'] or 0
  total_credit_sales=Credit.objects.aggregate(
    total_credit=Sum('amount_due')
  )['total_credit'] or 0

  total_sales=total_cash_sales+ total_credit_sales

  total_stock = Stock.objects.aggregate(
    total_quantity =Sum('tonnage')
  )['total_quantity'] or 0

  all_stocks =Stock.objects.all()
  grouped_stocks ={}

  for stock in all_stocks:
    if stock.name_of_produce not in grouped_stocks:
      grouped_stocks[stock.name_of_produce] ={
        'name':stock.name_of_produce,
      'branches':{},
      'total_quantity':0,
      }

    branch = stock.branch if stock.branch else 'Unknown'
    if branch not in grouped_stocks[stock.name_of_produce]['branches']:
      grouped_stocks[stock.name_of_produce]['branches'][branch] = 0 # Corrected line

    grouped_stocks[stock.name_of_produce]['branches'][branch] += stock.tonnage
    grouped_stocks[stock.name_of_produce]['total_quantity'] += stock.tonnage

  combined_stocks =list(grouped_stocks.values())
  recent_sales = Sales.objects.order_by('-id')[:10]

  context = {
    'total_cash_sales': total_cash_sales,
    'total_credit_sales': total_credit_sales,
    'total_sales': total_sales,
    'total_stock': total_stock,
    'combined_stocks': combined_stocks,
    'recent_sales': recent_sales, # Pass recent sales to the template
  }
  return render(request, 'dashboard2.html', context)


def salesagent(request):
    """
    Displays the dashboard page for sales agents, including total sales,
    stock summary, recent sales, and recent credit issued.
    """
    # Total Sales
    total_sales = Sales.objects.filter(salesagent_name=request.user).aggregate(
        total_sales=Sum('amount_paid')
    )['total_sales'] or 0

    # Stock Summary
    total_stock = Stock.objects.aggregate(total_tonnage=Sum('tonnage'))['total_tonnage'] or 0
    low_stock_threshold = 5  # You can adjust this threshold
    low_stock_products = Stock.objects.filter(tonnage__lt=low_stock_threshold)

    # Recent Sales (Let's get the last 5 sales, you can adjust the number)
    recent_sales = Sales.objects.filter(salesagent_name=request.user).order_by('-id')[:4] #ch
    # Recent Credit Issued (Let's get the last 5 credit entries)
    recent_credit = Credit.objects.order_by('-Dispatch_date')[:4]

    context = {
        'total_sales': total_sales,
        'total_stock': total_stock,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'recent_credit': recent_credit,
        'username': request.user.username,  # It's better to pass username explicitly
    }
    return render(request, 'dash1.html', context)

    
    

def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    

    return render(request, 'logout.html')

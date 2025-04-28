from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,Group




# Create User table called user profile using Abstract user from line 3
class Userprofile(AbstractUser):
    is_salesagent= models.BooleanField(default=False)
    is_manager= models.BooleanField(default=False)
    is_owner= models.BooleanField(default=False)
    username =models.CharField(max_length=25,unique=True)
    email =models.EmailField(max_length=25, unique=True)
    address = models.CharField(max_length=50, blank=True)
    phonenumber =models.CharField(max_length= 20,blank=True)
    gender = models.CharField(max_length=10, blank=True)
    # Override default reverse accessors to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="userprofile_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userprofile_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    def __str__(self):
        return self.username

#branch model
class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    def __str__(self):
        return self.branch_name

   
#produce model
class ProduceType(models.Model):
    type_of_produce = models.CharField(max_length=50)
    def __str__(self):
        return self.type_of_produce
                                


#stock model
class Stock(models.Model):
    name_of_produce=models.CharField(max_length =255)
    type_of_produce =models.ForeignKey(ProduceType,on_delete=models.CASCADE)
    date_and_time_of_produce= models.DateTimeField(auto_now_add =True)
    received_quantity = models.IntegerField(blank=False,null=True)
    issued_quantity=models.IntegerField(blank=False,null=True)
    tonnage =models.IntegerField(blank = False)
    cost=models.IntegerField(blank =False,default=25)   
    name_of_dealer=models.CharField(max_length=255)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE,null=True)
    contact=models.CharField(default=20)
    selling_price=models.IntegerField(null=True,blank=True)
    
#calculating the profit
    def profit_margin(self):
        return self.selling_price - self.cost

    def __str__(self):
        return self.name_of_produce
    
#sales table called sales    
class Sales(models.Model):
    product_name=models.ForeignKey(Stock, on_delete=models.CASCADE)
    tonnage=models.IntegerField()
    amount_paid =models.IntegerField(default=0,blank =False)
    buyers_name=models.CharField(max_length=35)
    date_and_time =models.DateTimeField(auto_now_add=True)
    salesagent_name=models.ForeignKey(Userprofile, on_delete=models.CASCADE,null=True)
    is_sold_on_cash=models.BooleanField(default=False)
    branch =models.ForeignKey(Branch, on_delete=models.CASCADE,null=True)
    selling_price=models.IntegerField(null=True,blank=True)

   
    

#calculating total_sales
    def total_sales(self):
        return self.product_name.selling_price * self.tonnage

    def calculate_change(self):
        total_sale = self.total_sales()
        if self.amount_paid is not None:
            change = self.amount_paid - total_sale
            return change
        return None
    def __str__(self):
        return self.buyers_name
       
#credit table      
class Credit(models.Model):
    buyer_name=models.CharField(max_length=255)
    NIN=models.CharField(unique=True)
    location=models.CharField(max_length=25,default=35)
    contact =models.IntegerField(default=20)
    amount_due=models.IntegerField(default=False)
    due_date=models.DateTimeField(auto_now_add=True)
    product_name=models.ForeignKey(Stock, on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True)
    salesagent_name=models.ForeignKey(Userprofile, on_delete=models.CASCADE,null=True)
    type_of_produce =models.ForeignKey(ProduceType,on_delete=models.CASCADE,null=True)
    tonnage =models.IntegerField(blank = False)
    Dispatch_date=models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.buyer_name     

from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class AddStockForm(ModelForm):
    class Meta:
        model=Stock
        fields='__all__'

class AddSalesForm(ModelForm):
    class Meta:
        model=Sales
        fields='__all__'

class AddCreditForm(ModelForm):
    class Meta:
        model=Credit
        fields='__all__'
        
class UpdateStockForm(ModelForm):
    class Meta:
        model=Stock
        fields='__all__'

class UserCreation(UserCreationForm):
    class Meta:
        model =Userprofile
        fields ='__all__'
    def save(self, commit="True"):
        user =super(UserCreation, self).save(commit=False)   
        if commit:
            user.is_active =True
            user.is_staff=True
            user.save()
            return user 

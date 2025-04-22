from django.forms import ModelForm
from .models import *


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
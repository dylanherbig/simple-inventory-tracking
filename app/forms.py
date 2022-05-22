from django import forms 
from .models import Warehouse, InventoryItem 

class WarehouseForm(forms.ModelForm):  
    class Meta:  
        model = Warehouse
        fields = '__all__'

class InventoryForm(forms.ModelForm):  
    class Meta:  
        model = InventoryItem
        fields = '__all__'
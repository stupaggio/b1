from django import forms
from .models import Checklist, Item

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ('list_name', 'list_code')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item', 'qty', 'comment', 'shop', 'action')
        
class List_code_Form(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ('list_code',)


from django import forms
from home.models import Product


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=15, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
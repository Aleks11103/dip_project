from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'city', 'address', 'postal_code']
        widgets = {
            'user': forms.HiddenInput(),
        }
    
    def clean(self):
        return self.cleaned_data
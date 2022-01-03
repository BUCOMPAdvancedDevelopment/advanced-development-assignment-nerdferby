from django import forms


class OrderForm(forms.Form):
    customer = forms.EmailField()
    product_id = forms.CharField(max_length=16)


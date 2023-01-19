from django import forms

class BuySecurityForm(forms.Form):
    amount = forms.FloatField(label='amount')

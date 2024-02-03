from django import forms
from django.forms import widgets

class send_email_form(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'subject', 'placeholder':'Заглавие'}), max_length=100, required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type':'email', 'class':'form-control', 'name':'email', 'placeholder':'Имейл'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'class':'form-control', 'name':'message', 'placeholder':'Съобщение'}), max_length=255, required=False)

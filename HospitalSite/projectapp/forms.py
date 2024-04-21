from django import forms
from django.forms import widgets
from .models import News_page

class send_email_form(forms.Form):
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'subject', 'placeholder':'Имейл'}), max_length=100, required=True)
    message = forms.CharField(label='',widget=forms.Textarea(attrs={'rows':'5', 'class':'form-control', 'name':'message', 'placeholder':'Съобщение'}), max_length=255, required=True)

class add_news_form(forms.ModelForm):
    class Meta:
        model = News_page
        fields = '__all__'
        labels = {
            'heading' : 'Заглавие',
            'content': 'Съдържание',
            'image' : 'Изображение',
            'author' : 'Автор',
            'date' : 'Дата',
            'time' : 'Времe'
        }
        widgets = {
            'heading' : forms.TextInput(),
            'description' : forms.Textarea(attrs={'rows': 4}),
            'image' : forms.FileInput(),
            'author' : forms.TextInput(),
            'date' : forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'time' : forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM:SS'})
        }
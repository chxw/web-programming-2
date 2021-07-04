from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject', 'class': 'form-control'
    }),label='Subject')
    context = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Describe, detail, or define your subject.', 'class': 'form-control'
    }), label='Context')

class EditEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject', 'class': 'form-control', 'disabled': True
    }),label='Subject')
    context = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Describe, detail, or define your subject.', 'class': 'form-control'
    }), label='Context')
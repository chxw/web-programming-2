from django import forms


class NewEntryForm(forms.Form):
    '''
    A Django Form object for new entries.

    User can input values via title (textinput widget) and
    context (textarea widget) to create a new entry.
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject', 'class': 'form-control', 'maxlength': 100
    }), label='Subject', max_length=100)
    context = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Describe, detail, or define your subject.',
        'class': 'form-control'
    }), label='Context')


class EditEntryForm(forms.Form):
    '''
    A Django Form object for editing entries.

    Title (textinput widget) is disabled. User can only input a value for
    context (textarea widget) to edit an existing entry.
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject', 'class': 'form-control', 'readonly': True
    }), label='Subject')
    context = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Describe, detail, or define your subject.',
        'class': 'form-control'
    }), label='Context')

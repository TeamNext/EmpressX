from django import forms


class AuthenticationForm(forms.Form):

    ticket = forms.SlugField(max_length=512)

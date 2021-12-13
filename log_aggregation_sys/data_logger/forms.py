from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'required': "required"}),
    )

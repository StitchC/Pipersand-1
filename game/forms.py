from django import forms


class long_loanForm(forms.Form):
    value = forms.IntegerField()
    year = forms.IntegerField()

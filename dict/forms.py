from django import forms


class WordForm(forms.Form):
    title = forms.CharField(
        label="Word",
        max_length=300,
    )

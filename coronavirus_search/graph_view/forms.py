from django import forms
from .new_cases import sorted_countries


class CountrySelectionForm(forms.Form):
    country_choices = sorted_countries()
    for i in range(len(country_choices)):
        country_choices[i] = (country_choices[i], country_choices[i])

    country = forms.ChoiceField(choices=country_choices)

from django.shortcuts import render
from . import forms
from .new_cases import draw_plot


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def visualisation(request):
    form = forms.CountrySelectionForm()
    context = {"form": form}
    return render(request, 'visualisation.html', context)


def visualisation2(request):
    form = forms.CountrySelectionForm()
    country = request.POST['country']
    context = {'graph': draw_plot(country), 'form': form}

    return render(request, 'visualisation2.html', context)


def avenir(request):
    return render(request, 'avenir.html')

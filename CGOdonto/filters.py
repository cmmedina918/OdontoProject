import django_filters
from django import forms
from .models import Turno, Paciente, Odontologo


class TurnoFilter(django_filters.FilterSet):

    paciente = django_filters.ModelChoiceFilter(
        queryset=Paciente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    odontologo = django_filters.ModelChoiceFilter(
        queryset=Odontologo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Turno
        fields = ['paciente', 'odontologo', 'fecha']

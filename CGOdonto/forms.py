from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import *

class procedimientoForm(forms.ModelForm):
    class Meta:
        model = Procedimiento
        fields = {'nombre'}
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control m-2',
            })
        }
        labels = {
            'nombre': 'Nombre del tratamiento',
        }

class enfermedadForm(forms.ModelForm):
    class Meta:
        model = Enfermedad
        fields = {'nombre'}
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control m-2',
            })
        }

class pacienteForm(forms.ModelForm):
    SEXO_CHOICES = (
        (True, 'Femenino'),
        (False, 'Masculino'),
    )

    embarazo = forms.TypedChoiceField(
        choices=((0, 'No'), (1, 'No sé'), (2, 'Sí')),
        coerce=int,
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=False,
    )
    anestesia = forms.TypedChoiceField(
        choices=((0, 'No'), (1, 'No sé'), (2, 'Sí')),
        coerce=int,
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )
    sexo = forms.TypedChoiceField(
        choices=SEXO_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )
    fuma = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Sí')),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )
    toma = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Sí')),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )
    cirugia = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Sí')),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )
    testElisa = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Sí')),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )
    transfucion = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Sí')),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )

    sangra = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Sí')),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={
            'class': 'm-2',
        }),
        required=True,
    )

    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ['status','fechaIngreso']
        widgets = {
            'fechaNacimieto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control m-2'},
                                              format='%Y-%m-%d'),
            'antecedentesFamiliares': forms.CheckboxSelectMultiple(),
            'nombreCompleto': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'CI': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control m-2',
                'rows': 2,
                'cols': 40,
            }),
            'transfucion': forms.CheckboxInput(attrs={
                'class': 'm-2',
            }),
            'transfucionMotivo': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'cirugiaMotivo': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'sangra': forms.CheckboxInput(attrs={
                'class': 'm-2',
            }),
            'haceCuantoToma': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'haceCuantoFuma': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'cuantoFuma': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'cuantoToma': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'semanasEmbarazo': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
            'haceCuantoTestElisa': forms.TextInput(attrs={
                'class': 'form-control m-2',
            }),
        }
        labels = {
            'nombreCompleto':'Nombre del paciente',
            'CI':'Número de cédula',
            'sexo':'Sexo',
            'fechaNacimieto':'Fecha de nacimiento',
            'transfucionMotivo':'Motivo de la transfución',
            'cirugiaMotivo':'Motivo de la cirugia',
            'haceCuantoFuma':'Hace cuanto fuma?',
            'cuantoFuma':'Cuanto fuma?',
            'haceCuantoToma':'Hace cuanto toma?',
            'cuantoToma':'Cuanto toma?',
            'semanasEmbarazo':'Cuantas semanas de embarazo?',
            'haceCuantoTestElisa':'Hace cuanto se realizo el test de elisa?',
            'testElisa':'Test de elisa',
            'antecedentesFamiliares':'Antecedentes familiares',
            'anestesia':'Es alergico/a a la anestesia?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fechaNacimieto:
            self.initial['fechaNacimieto'] = self.instance.fechaNacimieto.strftime('%Y-%m-%d')
        self.fields['antecedentesFamiliares'].required = False
        self.fields['antecedentesFamiliares'].queryset = Enfermedad.objects.filter(status=0)

    def clean_CI(self):
        ci = self.cleaned_data['CI']
        qs = Paciente.objects.filter(CI=ci)

        if self.instance.id:
            qs = qs.exclude(id=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un paciente con esta CI.")

        return ci

class turnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'
        exclude = ['status']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select select2',
            }),
            'odontologo': forms.Select(attrs={
                'class': 'form-select select2',
            }),
            'tratamiento': forms.Select(attrs={
                'class': 'form-select select2',
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().isoformat()
            }),
            'hora': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'min': '07:00',
                'max': '17:00',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(status=0)
        self.fields['odontologo'].queryset = Odontologo.objects.filter(status=0)
        self.fields['tratamiento'].queryset = Procedimiento.objects.filter(status=0)

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        odontologo = cleaned_data.get('odontologo')
        fecha = cleaned_data.get('fecha')

        if paciente and odontologo and fecha:
            turno_existente = Turno.objects.filter(
                paciente=paciente,
                odontologo=odontologo,
                fecha=fecha,
                status=0
            )

            if self.instance.pk:
                turno_existente = turno_existente.exclude(pk=self.instance.pk)

            if turno_existente.exists():
                raise ValidationError("Ya existe un turno para este paciente con este odontólogo en la fecha seleccionada.")

        return cleaned_data

class PlanTratamientoForm(forms.ModelForm):
    class Meta:
        model = PlanTratamiento
        fields = ['paciente', 'odotologo', 'diagnostico']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select select2',
            }),
            'odotologo': forms.Select(attrs={
                'class': 'form-select select2',
            }),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'paciente':'Seleccione un paciente',
            'odotologo': 'Seleccione un odontologo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(status=0)
        self.fields['odotologo'].queryset = Odontologo.objects.filter(status=0)

class PlanTratamientoProcedimientoForm(forms.ModelForm):
    class Meta:
        model = PlanTratamiento_Procedimiento
        fields = ['procedimento', 'diente', 'precio']
        widgets = {
            'procedimento': forms.Select(attrs={'class': 'form-control select2'}),
            'diente': forms.Select(attrs={'class': 'form-control select2'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EstadoDienteForm(forms.ModelForm):
    DELETE = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'hidden':True,
            }
        ),
        required=False
    )

    class Meta:
        model = EstadoDiente
        fields = ['diente','cara','estado', 'DELETE']
        widgets = {
            'diente': forms.Select(
                attrs={'class': 'form-control', 'hidden': True}
            ),
            'cara': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'estado': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

# Inline formset
PlanTratamientoProcedimientoFormSet = inlineformset_factory(
    PlanTratamiento,
    PlanTratamiento_Procedimiento,
    form=PlanTratamientoProcedimientoForm,
    extra=1,
    can_delete=True
)

OdontogramaEstadoDienteFormSet = inlineformset_factory(
    Odontograma,
    EstadoDiente,
    form=EstadoDienteForm,
    extra=1,
    can_delete=True,
    max_num = 4,
    validate_max = True
)
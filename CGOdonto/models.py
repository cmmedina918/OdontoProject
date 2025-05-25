from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# Create your models here.
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    precio = models.FloatField(null=False, blank=False, default=0)

    def __str__(self):
        return self.nombre

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombreCompleto = models.CharField(max_length=100, null=False, blank=False)
    CI = models.CharField(max_length=30, null=False, blank=False)
    fechaNacimieto = models.DateField(null=False, blank=False)
    sexo = models.BooleanField(null=False, blank=False, default=False)
    fechaIngreso = models.DateField(null=False, blank=False, default= now)
    telefono = models.CharField(max_length=30, null=False, blank=False)
    antecedentesFamiliares = models.ManyToManyField(Enfermedad)
    observaciones = models.TextField(null=False, blank=False, max_length=200)
    transfucion = models.BooleanField(default=False, null=False, blank=False)
    transfucionMotivo = models.CharField(max_length=100)
    cirugia = models.BooleanField(default=False, null=False, blank=False)
    cirugiaMotivo = models.CharField(max_length=100)
    sangra = models.BooleanField(default=False, null=False, blank=False)
    fuma = models.BooleanField(default=False, null=False, blank=False)
    haceCuantoFuma = models.CharField(max_length=100)
    cuantoFuma= models.CharField(max_length=100)
    toma = models.BooleanField(default=False, null=False, blank=False)
    haceCuantoToma = models.CharField(max_length=100)
    cuantoToma = models.CharField(max_length=100)
    embarazo = models.IntegerField(null=False, blank=False, default=0)
    semanasEmbarazo = models.IntegerField(default=0)
    anestesia = models.IntegerField(null=False, blank=False, default=0)
    testElisa = models.BooleanField(default=False, null=False, blank=False)
    haceCuantoTestElisa = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreCompleto

class Odontologo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    nro_cedula = models.CharField(max_length=20, null=False, default="0000", unique=True)
    nro_matricula = models.CharField(null=False, blank=False, default=0)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    odontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=False, blank=False)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.paciente.nombreCompleto

class PlanTratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    odotologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False, default=now)
    tratamiento = models.ManyToManyField(Tratamiento)

    def __str__(self):
        return self.paciente.nombreCompleto

class planTratamientoEntregas(models.Model):
    planTratamiento = models.ForeignKey(PlanTratamiento, on_delete=models.CASCADE, null=False, blank=False)
    monto = models.FloatField(null=False, blank=False, default=0)
    fecha = models.DateField(null=False, blank=False, default=now)

    def __str__(self):
        return self.planTratamiento.paciente.nombreCompleto
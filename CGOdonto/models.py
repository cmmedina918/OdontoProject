from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# Create your models here.
class Procedimiento(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    nombreCompleto = models.CharField(max_length=100, null=False, blank=False)
    CI = models.CharField(max_length=30, null=False, blank=False)
    fechaNacimieto = models.DateField(null=False, blank=False)
    sexo = models.BooleanField(null=False, blank=False, default=False)
    fechaIngreso = models.DateField(null=False, blank=False, auto_now_add=True)
    telefono = models.CharField(max_length=30, null=False, blank=False)
    antecedentesFamiliares = models.ManyToManyField(Enfermedad, blank=True)
    observaciones = models.TextField(null=True, blank=True, max_length=200)
    transfucion = models.BooleanField(default=False, null=False, blank=False)
    transfucionMotivo = models.CharField(null=True, blank=True,max_length=100)
    cirugia = models.BooleanField(default=False, null=False, blank=False)
    cirugiaMotivo = models.CharField(null=True, blank=True,max_length=100)
    sangra = models.BooleanField(default=False, null=False, blank=False)
    fuma = models.BooleanField(default=False, null=False, blank=False)
    haceCuantoFuma = models.CharField(null=True, blank=True,max_length=100)
    cuantoFuma= models.CharField(null=True, blank=True,max_length=100)
    toma = models.BooleanField(default=False, null=False, blank=False)
    haceCuantoToma = models.CharField(null=True, blank=True,max_length=100)
    cuantoToma = models.CharField(null=True, blank=True,max_length=100)
    embarazo = models.IntegerField(default=0)
    semanasEmbarazo = models.IntegerField(null=True, blank=True,default=0)
    anestesia = models.IntegerField(null=False, blank=False, default=0)
    testElisa = models.BooleanField(default=False, null=False, blank=False)
    haceCuantoTestElisa = models.CharField(null=True, blank=True,max_length=100)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.nombreCompleto

class Odontologo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    nro_cedula = models.CharField(max_length=20, null=False, default="0000", unique=True)
    nro_matricula = models.CharField(null=False, blank=False, default=0)
    telefono = models.CharField(max_length=20, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    odontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=False, blank=False)
    tratamiento = models.ForeignKey(Procedimiento, on_delete=models.CASCADE, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.paciente.nombreCompleto

class PlanTratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    odotologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False, default=now)
    tratamiento = models.ManyToManyField(Procedimiento, through='PlanTratamiento_Procedimiento')
    diagnostico = models.TextField(null=False, blank=False, max_length=200, default='')
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.paciente.nombreCompleto

class planTratamientoEntregas(models.Model):
    planTratamiento = models.ForeignKey(PlanTratamiento, on_delete=models.CASCADE, null=False, blank=False)
    monto = models.FloatField(null=False, blank=False, default=0)
    fecha = models.DateField(null=False, blank=False, default=now)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.planTratamiento.paciente.nombreCompleto

class Diente(models.Model):
    numero = models.CharField(max_length=2, unique=True)  # '11', '48', etc.
    cuadrante = models.IntegerField(choices=[(1, '1er - Superior Derecho'), (2, '2do - Superior Izquierdo'),
                                             (3, '3ro - Inferior Izquierdo'), (4, '4to - Inferior Derecho')])
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.numero

class Odontograma(models.Model):
    plan_tratamiento = models.OneToOneField(PlanTratamiento, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.plan_tratamiento.paciente.nombreCompleto}"

class EstadoDiente(models.Model):
    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE)
    diente = models.ForeignKey(Diente, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


    cara = models.CharField(max_length=1, choices=[
        ('V', 'Vestibular'),
        ('L', 'Lingual'),
        ('M', 'Mesial'),
        ('D', 'Distal'),
        ('O', 'Oclusal/Incisal'),
        ('T', 'Total')
    ])

    estado = models.CharField(max_length=1, choices=[
        ('C', 'Caries (Rojo)'),
        ('R', 'Restaurado (Azul)'),
        ('X', 'Extraído (Azul - A)'),
        ('E', 'A extraer (Rojo - /)'),
        ('G', 'Gingivitis (Rojo - G)'),
        ('P', 'Prótesis (Negro - P.F)'),
        ('M', 'Prótesis Removible (Azul - P.R)'),
        ('T', 'Endodoncia (Azul - T.C)'),
        ('S', 'Sellado (Azul - S)'),
    ])

    def __str__(self):
        return f"{self.diente.numero} - {self.cara} - {self.estado}"

class PlanTratamiento_Procedimiento(models.Model):
    planTratamiento = models.ForeignKey(PlanTratamiento, on_delete=models.CASCADE, null=False, blank=False)
    procedimento = models.ForeignKey(Procedimiento, on_delete=models.CASCADE, null=False, blank=False)
    diente = models.ForeignKey(Diente, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.FloatField(null=False, blank=False, default=0)


    def __str__(self):
        return f"{self.planTratamiento.paciente.nombreCompleto} - {self.procedimento.nombre}"

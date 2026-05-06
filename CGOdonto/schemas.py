from datetime import date

from ninja import ModelSchema

from CGOdonto.models import Paciente, Procedimiento, Enfermedad, Odontologo, Turno


class PacienteOut(ModelSchema):
    fechaNacimieto : date
    class Meta:
        model = Paciente
        fields = '__all__'

    @staticmethod
    def resolve_fechaNacimieto(obj):
        return obj.fechaNacimieto.date() if hasattr(obj.fechaNacimieto, "date") else obj.fechaNacimieto

class PacienteIn(ModelSchema):
    class Meta:
        model = Paciente
        exclude = ['id','status','fechaIngreso']

class ProcedimientoOut(ModelSchema):
    class Meta:
        model = Procedimiento
        fields = '__all__'

class ProcedimientoIn(ModelSchema):
    class Meta:
        model = Procedimiento
        exclude = ['id','status']

class EnfermedadOut(ModelSchema):
    class Meta:
        model = Enfermedad
        fields = '__all__'

class EnfermedadIn(ModelSchema):
    class Meta:
        model = Enfermedad
        exclude = ['id','status']

class OdontologoIn(ModelSchema):
    class Meta:
        model = Odontologo
        exclude = ['id','status']

class OdontologoOut(ModelSchema):
    class Meta:
        model = Odontologo
        fields = '__all__'

class TurnoOut(ModelSchema):
    class Meta:
        model = Turno
        fields = '__all__'

class TurnoIn(ModelSchema):
    class Meta:
        model = Turno
        exclude = ['id','status']
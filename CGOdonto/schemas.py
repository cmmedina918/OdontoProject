from ninja import ModelSchema

from CGOdonto.models import Paciente, Procedimiento, Enfermedad, Odontologo


class PacienteOut(ModelSchema):
    class Meta:
        model = Paciente
        fields = '__all__'

class PacienteIn(ModelSchema):
    class Meta:
        model = Paciente
        exclude = ['id','status']

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
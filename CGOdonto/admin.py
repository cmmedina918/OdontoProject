from django.contrib import admin

from CGOdonto.models import Turno, Odontologo, Paciente, Diente, Procedimiento, Odontograma

# Register your models here.
admin.site.register(Turno)
admin.site.register(Odontologo)
admin.site.register(Paciente)
admin.site.register(Diente)
admin.site.register(Procedimiento)
admin.site.register(Odontograma)
from django.contrib import admin

from CGOdonto.models import Turno, Odontologo, Paciente, Diente

# Register your models here.
admin.site.register(Turno)
admin.site.register(Odontologo)
admin.site.register(Paciente)
admin.site.register(Diente)
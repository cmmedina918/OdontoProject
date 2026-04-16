from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    # Procedimientos
    path('procedimiento/', views.procedimientos, name='procedimientos'),
    path('procedimiento/create/', views.procedimientoCreate, name='procedimientoCreate'),
    path('procedimiento/update/<int:id_procedimiento>', views.procedimientoUpdate, name='procedimientoUpdate'),
    path('procedimiento/delete/<int:id_procedimiento>', views.procedimientoDelete, name='procedimientoDelete'),
    # Pacientes
    path('paciente/', views.pacientes, name='pacientes'),
    path('paciente/deleted', views.pacientesDeleted, name='pacientesDeleted'),
    path('paciente/detail/<int:id_paciente>/', views.pacienteDetail, name='pacienteDetail'),
    path('paciente/detail/deleted/<int:id_paciente>', views.pacienteDetailDeleted, name='pacienteDetailDeleted'),
    path('paciente/create/', views.pacienteCreate, name='pacienteCreate'),
    path('paciente/update/<int:id_paciente>', views.pacienteUpdate, name='pacienteUpdate'),
    path('paciente/delete/<int:id_paciente>', views.pacienteDelete, name='pacienteDelete'),
    path('paciente/activate/<int:id_paciente>', views.pacienteActivate, name='pacienteActivate'),
    # Enfermedades
    path('enfermedad/', views.enfermedades, name='enfermedades'),
    path('enfermedad/create/', views.enfermedadCreate, name='enfermedadCreate'),
    path('enfermedad/update/<int:id_enfermedad>', views.enfermedadUpdate, name='enfermedadUpdate'),
    path('enfermedad/delete/<int:id_enfermedad>', views.enfermedadDelete, name='enfermedadDelete'),
    # Turnos
    path('turno', views.turnos, name='turnos'),
    path('turno/finished/', views.turnosFinished, name='turnosFinished'),
    path('turno/create/', views.turnoCreate, name='turnoCreate'),
    path('turno/update/<int:id_turno>', views.turnoUpdate, name='turnoUpdate'),
    path('turno/finish/<int:id_turno>', views.turnoFinish, name='turnoFinish'),
    path('turno/activate/<int:id_turno>', views.turnoActivate, name='turnoActivate'),
    # Plan de tratamiento
    path('plan/', views.planesTratamiento, name='planesTratamiento'),
    path('plan/create/', views.planTratamientoCreate, name='planCreate'),
    path('plan/detail/<int:id_plan>', views.planesTratamientoDetails, name='planDetail'),

    # Odontograma
    path('odontograma/create/<int:id_plan>/<int:id_odontograma>', views.odontogramaViewCreate, name='odontogramaCreate'),
]
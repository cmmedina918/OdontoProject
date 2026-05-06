from django.shortcuts import get_object_or_404
from ninja import Router

from CGOdonto.models import Turno, Odontologo, Paciente, Procedimiento
from CGOdonto.schemas import TurnoOut, TurnoIn

router = Router(tags=['turnos'])

@router.post('/create', response={201:TurnoIn})
def create_turno(request, payload: TurnoIn):
    data = payload.dict()

    paciente_id = data.pop('paciente')
    odontologo_id = data.pop('odontologo')
    tratamiento_id = data.pop('tratamiento')

    paciente = get_object_or_404(Paciente, id=paciente_id)
    odontologo = get_object_or_404(Odontologo, id=odontologo_id)
    tratamiento = get_object_or_404(Procedimiento, id=tratamiento_id)

    turno = Turno.objects.create(paciente=paciente, odontologo=odontologo,tratamiento=tratamiento, **data)
    return 201, turno

@router.get('/', response=list[TurnoOut])
def list_turnos(request):
    return Turno.objects.filter(status=0)

@router.get('/finished', response=list[TurnoOut])
def list_turnos_finished(request):
    return Turno.objects.filter(status=1)

@router.put('/{id_turno}', response=TurnoOut)
def get_turno(request, id_turno: int):
    turno = get_object_or_404(Turno, id=id_turno)
    if turno.status == 1:
        return 404, {'message': 'Turno no encontrado'}
    return turno

@router.put('/{id_turno}/finish', response={204:None})
def finish_turno(request, id_turno: int):
    turno = get_object_or_404(Turno, id=id_turno)
    turno.status = 1
    turno.save()
    return 204, None

@router.put('/{id_turno}/activate', response={204:None})
def activate_turno(request, id_turno: int):
    turno = get_object_or_404(Turno, id=id_turno)
    turno.status = 0
    turno.save()
    return 204, None

@router.delete('/{id_turno}', response={204:None})
def delete_turno(request, id_turno: int):
    turno = get_object_or_404(Turno, id=id_turno)
    turno.status = 3
    turno.save()
    return 204, None
from django.shortcuts import get_object_or_404
from ninja import Router

from CGOdonto.models import Odontologo
from CGOdonto.schemas import OdontologoOut, OdontologoIn

router = Router(tags=['odontologos'])

@router.post('/create', response={201: OdontologoOut})
def create_odontologo(request, payload: OdontologoIn):
    odontologo = Odontologo.objects.create(**payload.dict())
    return 201, odontologo

@router.put('/{id_odontologo}', response=OdontologoOut)
def update_odontologo(request, id_odontologo: int, payload: OdontologoIn):
    odontologo = get_object_or_404(Odontologo, id = id_odontologo)

    if odontologo.status == 1:
        return 400, {'message': 'Odontologo inactivo'}

    for attr, value in payload.dict().items():
        setattr(odontologo, attr, value)
    odontologo.save()
    return odontologo

@router.get('/{id_odontologo}', response=OdontologoOut)
def get_odontologo(request, id_odontologo: int):
    odontologo = get_object_or_404(Odontologo, id = id_odontologo)

    if odontologo.status == 1:
        return 404, {'message': 'Odontologo no encontrado'}

    return odontologo

@router.get('/', response=list[OdontologoOut])
def list_odontologos(request):
    return Odontologo.objects.filter(status=0)

@router.delete('/{id_odontologo}', response={204: None})
def delete_odontologo(request, id_odontologo: int):
    odontologo = get_object_or_404(Odontologo, id = id_odontologo)
    odontologo.status = 1
    odontologo.save()
    return 204, None
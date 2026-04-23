from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from CGOdonto.models import Enfermedad
from CGOdonto.schemas import EnfermedadOut, EnfermedadIn

router = Router(tags=['enfermedades'])


@router.post('/create', response={201 : EnfermedadOut})
def create_enfermedad(request, payload: EnfermedadIn):
    enfermedad = Enfermedad.objects.create(**payload.dict())
    return 201, enfermedad


@router.get('/{id_enfermedad}', response=EnfermedadOut)
def get_enfermedad(request, id_enfermedad: int):
    enfermedad = get_object_or_404(Enfermedad, id=id_enfermedad)

    if enfermedad.status == 1:
        return 404, {'message': 'Enfermedad no encontrada'}

    return enfermedad


@router.put('/{id_enfermedad}', response=EnfermedadOut)
def update_enfermedad(request, id_enfermedad: int, payload: EnfermedadIn):
    enfermedad = get_object_or_404(Enfermedad, id=id_enfermedad)

    if enfermedad.status == 1:
        return 400, {'message': 'Procedimiento inactivo'}

    for attr, value in payload.dict().items():
        setattr(enfermedad, attr, value)
    enfermedad.save()
    return enfermedad


@paginate
@router.get('/', response=list[EnfermedadOut])
def list_enfermedades(request):
    return Enfermedad.objects.filter(status=0)


@router.delete('/{id_enfermedad}', response={204: None})
def delete_enfermedad(request, id_enfermedad: int):
    enfermedad = get_object_or_404(Enfermedad, id=id_enfermedad)
    enfermedad.status = 1
    enfermedad.save()
    return 204, None
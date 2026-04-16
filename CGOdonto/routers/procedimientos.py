from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from CGOdonto.models import Procedimiento
from CGOdonto.schemas import ProcedimientoOut, ProcedimientoIn

router = Router(tags=['procedimientos'])

@paginate
@router.get('/', response=list[ProcedimientoOut])
def list_procedimientos(request):
    return Procedimiento.objects.filter(status=0)


@router.get('/{id_procedimiento}', response=ProcedimientoOut)
def get_procedimiento(request, id_procedimiento: int):
    procedimiento = get_object_or_404(Procedimiento, id=id_procedimiento)

    if procedimiento.status == 1:
        return 404, {'message': 'Procedimiento no encontrado'}

    return procedimiento


@router.post('/create', response={201: ProcedimientoOut})
def create_procedimiento(request, payload: ProcedimientoOut):
    procedimiento = Procedimiento.objects.create(**payload.dict())
    return 201, procedimiento


@router.put('/{id_procedimiento}', response=ProcedimientoOut)
def update_procedimiento(request, id_procedimiento: int, payload: ProcedimientoIn):
    procedimiento = get_object_or_404(Procedimiento, id=id_procedimiento)

    if procedimiento.status == 1:
        return 400, {'message': 'Procedimiento inactivo'}

    for attr, value in payload.dict().items():
        setattr(procedimiento, attr, value)
    procedimiento.save()
    return procedimiento


@router.delete('/{id_procedimiento}', response={204: None})
def delete_procedimiento(request, id_procedimiento: int):
    procedimiento = get_object_or_404(Procedimiento, id=id_procedimiento)
    procedimiento.status = 1
    procedimiento.save()
    return 204, None
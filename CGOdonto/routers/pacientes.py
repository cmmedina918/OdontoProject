from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from CGOdonto.models import Paciente
from CGOdonto.schemas import PacienteOut, PacienteIn

router = Router(tags=['pacientes'])


@router.post('/create', response={201: PacienteOut})
def create_paciente(request, payload: PacienteIn):
    data = payload.dict()
    antecedentes = data.pop('antecedentesFamiliares', [])

    paciente = Paciente.objects.create(**data)

    if antecedentes:
        paciente.antecedentesFamiliares.set(antecedentes)

    return 201, paciente


@router.put('/{id_paciente}', response=PacienteOut)
def update_paciente(request, id_paciente: int, payload: PacienteIn):
    paciente = get_object_or_404(Paciente, id=id_paciente)

    if paciente.status == 1:
        return 400, {'message': 'Paciente inactivo'}

    data = payload.dict(exclude_unset=True)

    antecedentes = data.pop('antecedentesFamiliares', None)

    for attr, value in data.items():
        setattr(paciente, attr, value)

    paciente.save()

    if antecedentes is not None:
        paciente.antecedentesFamiliares.set(antecedentes)

    return paciente


@router.get('/{id_paciente}', response=PacienteOut)
def get_paciente(request, id_paciente: int):
    return get_object_or_404(Paciente, id=id_paciente)


@paginate
@router.get('/', response=list[PacienteOut])
def list_pacientes(request):
    return Paciente.objects.filter(status=0)


@router.delete('/{id_paciente}', response={204: None})
def delete_paciente(request, id_paciente: int):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    paciente.status = 1
    paciente.save()
    return 204, None
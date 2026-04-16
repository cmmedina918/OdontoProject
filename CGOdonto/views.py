from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .filters import TurnoFilter
from .forms import *
from .models import *
from .utils import quitar_acentos

# Create your views here.
def test(request):
    return render(request,'base.html')

# <-- Procedimientos -->
def procedimientos(request):
    procedimientos = Procedimiento.objects.all().filter(status=0)
    paginator = Paginator(procedimientos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'procedimientos.html', {'page_obj':page_obj})

def procedimientoCreate(request):
    if request.method == "POST":
        form = procedimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('procedimientos')
        else:
            return render(request, 'forms/procedimiento.html', {'form': form})
    else:
        form = procedimientoForm()
        return render(request, 'forms/procedimiento.html', {'form':form})

def procedimientoUpdate(request, id_procedimiento):
    procedimiento = Procedimiento.objects.get(id = id_procedimiento)
    if request.method == "POST":
        form = procedimientoForm(request.POST, instance = procedimiento)
        if form.is_valid():
            form.save()
            return redirect('procedimientos')
        else:
            return render(request, 'forms/procedimiento.html', {'form': form})
    else:
        form = procedimientoForm(instance = procedimiento)
        return render(request, 'forms/procedimiento.html', {'form': form})

def procedimientoDelete(request, id_procedimiento):
    procedimiento = get_object_or_404(Procedimiento, id = id_procedimiento)
    if request.method == "POST":
        procedimiento.status = 1
        procedimiento.save()
        return redirect('procedimientos')

# <-- Pacientes -->
def pacientes(request):
    query = request.GET.get('q')
    pacientes = Paciente.objects.filter(status=0)

    if query:
        texto_normalizado = quitar_acentos(query).lower()
        pacientes = [
            paciente for paciente in pacientes
            if texto_normalizado in quitar_acentos(paciente.nombreCompleto).lower()
               or texto_normalizado in quitar_acentos(paciente.CI).lower()
        ]

    paginator = Paginator(pacientes, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'pacientes.html',{'page_obj': page_obj,'query': query,})

def pacientesDeleted(request):
    query = request.GET.get('q')
    pacientes = Paciente.objects.filter(status=1)

    if query:
        texto_normalizado = quitar_acentos(query).lower()
        pacientes = [
            paciente for paciente in pacientes
            if texto_normalizado in quitar_acentos(paciente.nombreCompleto).lower()
               or texto_normalizado in quitar_acentos(paciente.CI).lower()
        ]

    paginator = Paginator(pacientes, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'pacientesDeleted.html',{'page_obj': page_obj,'query': query,})

def pacienteDetail(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    return render(request,'pacienteDetalles.html',{'paciente':paciente})

def pacienteDetailDeleted(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    return render(request,'pacienteDetallesDeleted.html',{'paciente':paciente})

def pacienteCreate(request):
    if request.method == "POST":
        form = pacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit = False)
            paciente.save()
            form.save_m2m()
            return redirect('pacientes')
        else:
            return render(request, 'forms/paciente.html', {'form': form,
                                                                                'modo': 'create'})
    else:
        form = pacienteForm()
        return render(request, 'forms/paciente.html', {'form': form,
                                                                            'modo': 'create'})

def pacienteUpdate(request, id_paciente):
    paciente = get_object_or_404(Paciente, id = id_paciente)
    if request.method == "POST":
        form = pacienteForm(request.POST, instance = paciente)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.save()
            form.save_m2m()
            return redirect('pacienteDetail', id_paciente)
        else:
            return render(request, 'forms/paciente.html', {'form': form,
                                                                                'modo': 'update'})
    else:
        form = pacienteForm(instance = paciente)
        return render(request, 'forms/paciente.html', {'form': form,
                                                                            'modo': 'update'})

def pacienteDelete(request, id_paciente):
    paciente = get_object_or_404(Paciente, id = id_paciente)
    if request.method == "POST":
        paciente.status = 1
        paciente.save()
        return redirect('pacientes')

def pacienteActivate(request, id_paciente):
    paciente = get_object_or_404(Paciente, id = id_paciente)
    if request.method == "POST":
        paciente.status = 0
        paciente.save()
        return redirect('pacientes')

# <-- Enfermedad -->
def enfermedades(request):
    enfermedades = Enfermedad.objects.all().filter(status=0)
    paginator = Paginator(enfermedades, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'enfermedades.html',{'page_obj':page_obj})

def enfermedadCreate(request):
    if request.method == "POST":
        form = enfermedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enfermedades')
        else:
            return render(request, 'forms/enfermedad.html', {'form': form})
    else:
        form = enfermedadForm()
        return render(request, 'forms/enfermedad.html', {'form': form})

def enfermedadUpdate(request, id_enfermedad):
    enfermedad = Enfermedad.objects.get(id = id_enfermedad)
    if request.method == "POST":
        form = enfermedadForm(request.POST, instance = enfermedad)
        if form.is_valid():
            form.save()
            return redirect('enfermedades')
        else:
            return render(request, 'forms/enfermedad.html', {'form': form})
    else:
        form = enfermedadForm(instance = enfermedad)
        return render(request, 'forms/enfermedad.html', {'form': form})

def enfermedadDelete(request, id_enfermedad):
    enfermedad = get_object_or_404(Enfermedad, id = id_enfermedad)
    if request.method == "POST":
        enfermedad.status = 1
        enfermedad.save()
        return redirect('enfermedades')

# <-- Turnos -->
def turnos(request):
    turnos_queryset = Turno.objects.filter(status=0).order_by('-fecha', '-hora')
    turno_filter = TurnoFilter(request.GET, queryset=turnos_queryset)

    paginator = Paginator(turno_filter.qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'turnos.html', {
        'filter': turno_filter,
        'page_obj': page_obj,
    })

def turnosFinished(request):
    turnos_queryset = Turno.objects.filter(status=1).order_by('-fecha', '-hora')
    turno_filter = TurnoFilter(request.GET, queryset=turnos_queryset)

    paginator = Paginator(turno_filter.qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'turnosFinalizados.html', {
        'filter': turno_filter,
        'page_obj': page_obj,
    })

def turnoCreate(request):
    if request.method == "POST":
        form = turnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turnos')
        else:
            return render(request, 'forms/turno.html', {'form': form, 'modo':'create'})
    else:
        form = turnoForm()
        return render(request, 'forms/turno.html', {'form': form, 'modo':'create'})

def turnoUpdate(request, id_turno):
    turno = get_object_or_404(Turno, id = id_turno)
    if request.method == "POST":
        form = turnoForm(request.POST, instance = turno)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
        else:
            return render(request, 'forms/turno.html', {'form': form, 'modo':'update'})
    else:
        form = turnoForm(instance = turno)
        return render(request, 'forms/turno.html', {'form': form, 'modo':'update'})

def turnoFinish(request, id_turno):
    turno = get_object_or_404(Turno, id = id_turno)
    if request.method == "POST":
        turno.status = 1
        turno.save()
        return redirect('turnos')

def turnoActivate(request, id_turno):
    turno = get_object_or_404(Turno, id = id_turno)
    if request.method == "POST":
        turno.status = 0
        turno.save()
        return redirect('turnos')

# <-- Plan de tratamiento -->
def planesTratamiento(request):
    query = request.GET.get('q')
    planesTratamiento_qs = PlanTratamiento.objects.filter(status=0).prefetch_related(
        'plantratamiento_procedimiento_set__procedimento',
        'paciente'
    )

    if query:
        texto_normalizado = quitar_acentos(query).lower()
        planesTratamiento_qs = [
            plan for plan in planesTratamiento_qs
            if texto_normalizado in quitar_acentos(plan.paciente.nombreCompleto).lower()
               or texto_normalizado in quitar_acentos(plan.paciente.CI).lower()
        ]

    for plan in planesTratamiento_qs:
        plan.total = sum(p.precio for p in plan.plantratamiento_procedimiento_set.all())

    paginator = Paginator(planesTratamiento_qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'planesTratamiento.html', {
        'page_obj': page_obj,
        'query': query,
    })

def planesTratamientoDetails(request, id_plan):
    plan = get_object_or_404(PlanTratamiento, id = id_plan)
    odontograma = get_object_or_404(Odontograma, plan_tratamiento = plan)
    return render(request, 'planDetails.html', { 'plan':plan, 'odontograma': odontograma})

def planTratamientoCreate(request):
    if request.method == 'POST':
        form = PlanTratamientoForm(request.POST)
        formset = PlanTratamientoProcedimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            plan = form.save()
            formset.instance = plan
            formset.save()

            odontograma = Odontograma.objects.create(plan_tratamiento=plan)

            return redirect('odontogramaCreate',
                            id_plan = plan.id,
                            id_odontograma = odontograma.id)
    else:
        form = PlanTratamientoForm()
        formset = PlanTratamientoProcedimientoFormSet()

    return render(request, 'forms/planTratamiento.html', {
        'form': form,
        'formset': formset,
        'modo': 'crear'
    })

# <-- Odontogramas -->
def odontogramaViewCreate(request, id_plan, id_odontograma):
    plan = get_object_or_404(PlanTratamiento, id=id_plan)
    odontograma = get_object_or_404(Odontograma, id=id_odontograma, plan_tratamiento=plan)

    if request.method == 'POST':
        formset = OdontogramaEstadoDienteFormSet(request.POST, instance=odontograma)
        if formset.is_valid():
            formset.save()
            formset = OdontogramaEstadoDienteFormSet(instance=odontograma)
    else:
        formset = OdontogramaEstadoDienteFormSet(instance=odontograma)

    return render(request, 'forms/odontograma.html', {
        'modo': 'crear',
        'range_8': range(8,0,-1),
        'formset': formset,
    })
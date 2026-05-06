from ninja import NinjaAPI
from CGOdonto.routers.pacientes import router as pacientes_routes
from CGOdonto.routers.procedimientos import router as procedimientos_routes
from CGOdonto.routers.enfermedades import router as enfermedades_routes
from CGOdonto.routers.odontologos import router as odontologos_routes
from CGOdonto.routers.turnos import router as turnos_routes

api = NinjaAPI(
    title="API Odontológica",
    description="API para gestión de pacientes y tratamientos",
    version="1.0.0"
)

api.add_router("/pacientes/", pacientes_routes)
api.add_router("/procedimientos/", procedimientos_routes)
api.add_router("/enfermedades/", enfermedades_routes)
api.add_router("/odontologos/", odontologos_routes)
api.add_router("/turnos/", turnos_routes)
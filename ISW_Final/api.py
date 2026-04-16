from ninja import NinjaAPI
from CGOdonto.routers.pacientes import router as pacientes_routes
from CGOdonto.routers.procedimientos import router as procedimientos_routes

api = NinjaAPI(
    title="API Odontológica",
    description="API para gestión de pacientes y tratamientos",
    version="1.0.0"
)

api.add_router("/pacientes/", pacientes_routes)
api.add_router("/procedimientos/", procedimientos_routes)
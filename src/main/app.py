from fastapi import FastAPI
from src.main.routes.api.user.user_routes import routes as user_routes
from src.main.routes.api.bairro.bairro_routes import routes as bairro_routes
from src.main.routes.api.empresa.empresa_routes import routes as empresa_routes
from src.main.routes.api.fiscal.fiscal_routes import routes as fiscal_routes

app = FastAPI()
app.include_router(user_routes)
app.include_router(bairro_routes)
app.include_router(empresa_routes)
app.include_router(fiscal_routes)
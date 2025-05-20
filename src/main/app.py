from fastapi import FastAPI
from src.main.routes.api.user.user_routes import routes as user_routes
from src.main.routes.api.bairro.bairro_routes import routes as bairro_routes
from src.main.routes.api.empresa.empresa_routes import routes as empresa_routes
from src.main.routes.api.fiscal.fiscal_routes import routes as fiscal_routes
from src.main.routes.api.history_project.history_project_routes import routes as history_project_routes
from src.main.routes.api.auth.login_routes import routes as auth_routes
from src.main.routes.api.project.project_routes import routes as project_routes
from src.main.routes.api.project_bairro.project_bairro_routes import routes as project_bairro_routes
from src.main.routes.api.project_empresa.project_empresa_routes import routes as project_empresa_routes

app = FastAPI()
app.include_router(user_routes)
app.include_router(bairro_routes)
app.include_router(empresa_routes)
app.include_router(fiscal_routes)
app.include_router(history_project_routes)
app.include_router(auth_routes)
app.include_router(project_routes)
app.include_router(project_bairro_routes)
app.include_router(project_empresa_routes)
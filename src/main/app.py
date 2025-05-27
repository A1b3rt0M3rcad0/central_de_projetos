#pylint:disable=C0413
from fastapi import FastAPI

# Routes
from src.main.routes.api.user.user_routes import routes as user_routes
from src.main.routes.api.bairro.bairro_routes import routes as bairro_routes
from src.main.routes.api.empresa.empresa_routes import routes as empresa_routes
from src.main.routes.api.fiscal.fiscal_routes import routes as fiscal_routes
from src.main.routes.api.history_project.history_project_routes import routes as history_project_routes
from src.main.routes.api.auth.login_routes import routes as auth_routes
from src.main.routes.api.project.project_routes import routes as project_routes
from src.main.routes.api.project_bairro.project_bairro_routes import routes as project_bairro_routes
from src.main.routes.api.project_empresa.project_empresa_routes import routes as project_empresa_routes
from src.main.routes.api.project_type.project_type_routes import routes as project_type_routes
from src.main.routes.api.status.status_routes import routes as status_routes
from src.main.routes.api.user_project.user_project_routes import routes as user_project_routes
from src.main.routes.api.document.document_routes import routes as document_routes
from src.main.routes.api.types.types_routes import routes as types_routes

# Web
from src.main.routes.web.login.routes_login import routes as login_web

app = FastAPI()

# Test Route
from src.main.routes.middleware.test_routes import routes as test_route

app.include_router(test_route)

# Routes
app.include_router(user_routes)
app.include_router(bairro_routes)
app.include_router(empresa_routes)
app.include_router(fiscal_routes)
app.include_router(history_project_routes)
app.include_router(auth_routes)
app.include_router(project_routes)
app.include_router(project_bairro_routes)
app.include_router(project_empresa_routes)
app.include_router(project_type_routes)
app.include_router(status_routes)
app.include_router(user_project_routes)
app.include_router(document_routes)
app.include_router(types_routes)

# Web
app.include_router(login_web)

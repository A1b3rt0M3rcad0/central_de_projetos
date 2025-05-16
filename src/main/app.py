from fastapi import FastAPI
from src.main.routes.api.user.user_routes import routes as user_routes
from src.main.routes.api.bairro.bairro_routes import routes as bairro_routes

app = FastAPI()
app.include_router(user_routes)
app.include_router(bairro_routes)
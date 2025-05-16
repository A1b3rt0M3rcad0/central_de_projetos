from fastapi import FastAPI
from src.main.routes.api.user.user_routes import routes as user_routes

app = FastAPI()
app.include_router(user_routes)
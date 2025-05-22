#pylint:disable=all
from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.main.routes.middleware.authorization import get_current_user, role_required

routes = APIRouter(prefix="/test", tags=["Test"])

@routes.get("/secure")
def secure_route(user = Security(role_required(['ADMIN']))):
    return {"msg": "Você está autenticado!", "user": user}
#pylint:disable=all
from fastapi import APIRouter, Security
from fastapi import Request
from src.main.routes.middleware.authorization import role_required

routes = APIRouter(prefix="/test", tags=["Test"])

@routes.get("/secure")
def secure_route(request:Request, user = Security(role_required(['ADMIN', 'VEREADOR']))):
    if request.state.new_access_token:
        return {"access_token": request.state.new_access_token,"msg": "Você está autenticado!", "user": user}
    return {"msg": "Você está autenticado!", "user": user}

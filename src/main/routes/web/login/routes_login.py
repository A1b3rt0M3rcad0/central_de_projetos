#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.templates.config import templates

routes = APIRouter(prefix='/web', tags=['auth', 'login'])

@routes.get('/login')
async def login(request:Request):
    return templates.TemplateResponse(
        "login/index.html", {"request":request, "test": "Olá Mundo"}
    )
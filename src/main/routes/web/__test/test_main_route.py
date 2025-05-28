#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.templates.config import templates

routes = APIRouter(prefix='/test', tags=['auth', 'login'])

@routes.get('/base_template')
async def base_template_test(request: Request):
    projetos = {
        "projetos": [
            {
                "id": 1,
                "status": "Em Projeto",
                "name": "Projeto Alpha",
                "verba_disponivel": 123456.78,
                "andamento_do_projeto": "50%",
                "start_date": None,
                "expected_completion_date": None,
                "end_date": None,
            },
            {
                "id": 2,
                "status": "Licitação",
                "name": "Projeto Beta",
                "verba_disponivel": 98765.43,
                "andamento_do_projeto": "75%",
                "start_date": None,
                "expected_completion_date": None,
                "end_date": None,
            }
        ]
    }

    return templates.TemplateResponse(
        "content/project_row.html",
        {
            "request": request,
            "projetos": projetos["projetos"],
            "title": "Lista de projetos"
        }
    )

@routes.get('/base_project_view')
async def project_view_test(request: Request):
    projeto = {
        "id": 123,
        "nome": "Avenida Brasil",
        "status_projeto": {"nome": "Em andamento"},
        "verba_disponivel": 1500000.75,
        "andamento": 65,
        "data_inicio": "2024-01-15",
        "previsao_conclusao": "2024-12-20",
        "data_termino": None,
        "bairro": {"nome": "Centro"},
        "empresa": {"nome": "Construtora ABC Ltda."},
        "fiscal": {"nome": "João Silva"},
        "tipo_projeto": {"nome": "Infraestrutura Urbana"},
        "vereador_responsavel": {"nome": "Carlos Pereira", "cpf": "12345678901"},
        "documentos": [
            {"nome": "Contrato Principal", "tipo_arquivo": "PDF", "tamanho": "2.4 MB", "url": "#"},
            {"nome": "Licença Ambiental", "tipo_arquivo": "PDF", "tamanho": "1.1 MB", "url": "#"},
        ],
        "historico": [
            {"data": "2024-02-10 14:30", "campo": "Verba Disponível", "descricao": "Verba aumentada em R$ 500.000,00."},
            {"data": "2024-03-05 09:15", "campo": "Andamento", "descricao": "Obra atingiu 30% de execução física."},
        ]
    }

    return templates.TemplateResponse(
        "content/project_view.html",
        {
            "request": request,
            "projeto": projeto,
            "title": projeto["nome"]
        }
    )
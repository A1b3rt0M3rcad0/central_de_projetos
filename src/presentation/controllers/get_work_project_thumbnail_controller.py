from src.domain.use_cases.i_get_latest_work_project_image import IGetLatestWorkProjectImage
from src.domain.use_cases.i_verify_fiscal_work_project_association import IVerifyFiscalWorkProjectAssociation
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors.use_cases.unauthorized_access_error import UnauthorizedAccessError
import os

class GetWorkProjectThumbnailController(ControllerInterface):

    def __init__(self, 
                 get_latest_work_project_image_case: IGetLatestWorkProjectImage,
                 verify_fiscal_work_project_association_case: IVerifyFiscalWorkProjectAssociation) -> None:
        self.__get_latest_work_project_image_case = get_latest_work_project_image_case
        self.__verify_fiscal_work_project_association_case = verify_fiscal_work_project_association_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Obter dados do path_params e body
            path_params = http_request.path_params or {}
            body = http_request.body or {}
            
            work_project_id = int(path_params.get('work_project_id'))
            fiscal_id = body.get('fiscal_id')
            
            if not fiscal_id:
                raise UnauthorizedAccessError(
                    message="Fiscal ID não encontrado na requisição"
                )
            
            # Validação: Verificar se o fiscal está associado ao work project
            is_associated = self.__verify_fiscal_work_project_association_case.verify(
                fiscal_id=fiscal_id,
                work_project_id=work_project_id
            )
            
            if not is_associated:
                raise UnauthorizedAccessError(
                    message=f"Fiscal não está autorizado a acessar este work project. Work Project ID: {work_project_id}"
                )
            
            # Tentar obter a última imagem do work project
            image_data = self.__get_latest_work_project_image_case.get_latest_image(work_project_id)
            
            if image_data:
                # Retornar a imagem encontrada
                return HttpResponse(
                    status_code=200,
                    body=image_data,
                    headers={
                        'Content-Type': 'image/jpeg',
                        'Cache-Control': 'public, max-age=86400',  # Cache por 24 horas
                        'ETag': f'wp-{work_project_id}-{hash(image_data) % 1000000}'
                    }
                )
            
            # Retornar SVG default
            svg_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'default_thumbnail.svg')
            
            try:
                with open(svg_path, 'rb') as f:
                    svg_data = f.read()
                
                return HttpResponse(
                    status_code=200,
                    body=svg_data,
                    headers={
                        'Content-Type': 'image/svg+xml',
                        'Cache-Control': 'public, max-age=86400',  # Cache por 24 horas
                        'ETag': f'wp-{work_project_id}-default'
                    }
                )
            except FileNotFoundError:
                # Se o SVG não for encontrado, retornar erro
                return HttpResponse(
                    status_code=404,
                    body={'error': 'Thumbnail não encontrada'}
                )
            
        except Exception as e:
            raise e from e 
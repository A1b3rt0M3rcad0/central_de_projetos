from src.domain.use_cases.i_find_all_bairro import IFindAllBairro
from src.domain.use_cases.i_find_all_empresas import IFindAllEmpresas
from src.domain.use_cases.i_find_all_fiscal import IFindAllFiscal
from src.domain.use_cases.i_find_all_types import IFindAllTypes
from src.domain.use_cases.i_find_all_user_by_role import IFindAllUserByRole
from src.domain.value_objects.roles import Role
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class FindAllAssociationsPossiblityFromProjectController(ControllerInterface):

    def __init__(self, 
                 find_all_bairro:IFindAllBairro, 
                 find_all_empresas:IFindAllEmpresas, 
                 find_all_fiscal:IFindAllFiscal,
                 find_all_types:IFindAllTypes,
                 find_all_user_by_role:IFindAllUserByRole
                 ) -> None:
        self.__find_all_bairro = find_all_bairro
        self.__find_all_empresas = find_all_empresas
        self.__find_all_fiscal = find_all_fiscal
        self.__find_all_types = find_all_types
        self.__find_all_user_by_role = find_all_user_by_role
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            bairros = self.__find_all_bairro.find()
            empresas = self.__find_all_empresas.find()
            fiscais = self.__find_all_fiscal.find()
            types = self.__find_all_types.find()
            vereadores = self.__find_all_user_by_role.find(role=Role('vereador'))
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Possibly Associatons founded",
                    "content": {
                        "bairro": [
                            {
                                "id": bairro.bairro,
                                "name": bairro.name
                            }
                            for bairro in bairros
                        ],
                        "empresa": [
                            {
                                "id": empresa.empresa_id,
                                "name": empresa.name
                            }
                            for empresa in empresas
                        ],
                        "fiscal": [
                            {
                                "id": fiscal.fiscal_id,
                                "name": fiscal.name
                            }
                            for fiscal in fiscais
                        ],
                        "type": [
                            {
                                "id": type_s.types_id,
                                "name": type_s.name
                            }
                            for type_s in types
                        ],
                        "vereador": [
                            {
                                "id": vereador.cpf.value,
                                "name": vereador.name
                            }
                            for vereador in vereadores
                        ]
                    }
                }
            )
        except Exception as e:
            raise e from e
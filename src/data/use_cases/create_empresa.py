from src.domain.use_cases.i_create_empresa import ICreateEmpresa
from src.data.interface.i_empresa_repository import IEmpresaRepository

class CreateEmpresa(ICreateEmpresa):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository = empresa_repository
    
    def create(self, name:str) -> None:
        try:
            self.__empresa_repository.insert(
                name=name
            )
        except Exception as e:
            raise e from e
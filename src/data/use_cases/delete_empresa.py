from src.domain.use_cases.i_delete_empresa import IDeleteEmpresa
from src.data.interface.i_empresa_repository import IEmpresaRepository

class DeleteEmpresa(IDeleteEmpresa):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository = empresa_repository
    
    def delete(self, name:str) -> None:
        try:
            self.__empresa_repository.delete(
                name=name
            )
        except Exception as e:
            raise e from e
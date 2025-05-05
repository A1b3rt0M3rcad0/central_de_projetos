from src.data.interface.i_empresa_repository import IEmpresaRepository
from src.domain.use_cases.i_update_empresa import IUpdateEmpresa

class UpdateEmpresa(IUpdateEmpresa):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository = empresa_repository
    
    def update(self, name:str, new_name:str) -> None:
        try:
            self.__empresa_repository.update(
                name=name,
                new_name=new_name
            )
        except Exception as e:
            raise e from e
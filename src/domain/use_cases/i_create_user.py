from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from abc import ABC, abstractmethod

class ICreateUser(ABC):

    @abstractmethod
    def create(self, cpf:CPF, email:Email, role:Role, password:Password) -> None:
        '''
        coleta o cpf, email, role e password, para criar um usuario, para criar o usuario e salvar no banco de dados primeiro e necessario
        cruptografar e fazer hashedpassword no coletando o password hashedado e o salt para salvar no banco de dados,
        caso no consiga criar o usuario:
        usuario ja existe (cpf): 400, CpfAlreadyExistsError
        cpf com formato incorreto: 400 InvalidCpfError
        email ja existe: 400, EmailAlreadyExistsError
        email com formato incorreto: 400, InvalidEmailError
        password com formato incorreto: 400, InvalidPasswordError
        não consegue por outro motivo: 500, UserNotCreatedError
        '''
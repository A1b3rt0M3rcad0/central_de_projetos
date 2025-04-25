from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from abc import ABC, abstractmethod

class ICreateUser(ABC):

    @abstractmethod
    def create(self, cpf:CPF, email:Email, role:Role, password:Password) -> None:
        """
        Cria um novo usuário no sistema.

        Antes de salvar no banco de dados, a senha é criptografada e transformada em um hash com salt.

        Parâmetros:
            cpf: CPF do usuário.
            email: Endereço de e-mail do usuário.
            role: Papel do usuário no sistema.
            password: Senha em texto plano que será criptografada.

        Levanta:
            InvalidCpfError (400): Se o CPF estiver em formato inválido.
            InvalidEmailError (400): Se o e-mail estiver em formato inválido.
            InvalidPasswordError (400): Se a senha não atender aos critérios de segurança.
            UserNotCreatedError (500): Para qualquer outro erro ao tentar criar o usuário.
        """
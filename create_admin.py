#pylint:disable=W0718
import argparse
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from src.data.use_cases.create_user import CreateUser
from src.data.use_cases.create_refresh_token import CreateRefreshToken
from src.infra.relational.repository.user_repository import UserRepository
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from getpass import getpass

def main():
    parser = argparse.ArgumentParser(description="Criar usuário admin")
    parser.add_argument("-c", "--cpf", required=True, help="CPF do admin")
    parser.add_argument("-e", "--email", required=True, help="Email do admin")
    parser.add_argument("-n", "--name", help="Nome do admin")
    args = parser.parse_args()

    password = getpass("Senha do admin: ")
    password_confirm = getpass("Confirme a senha: ")
    if password != password_confirm:
        print("Senhas não conferem.")
        return

    try:
        cpf_vo = CPF(args.cpf)
        email_vo = Email(args.email)
        password_vo = Password(password)
        role_vo = Role("admin")  # papel admin fixo

        repo = UserRepository(
            db_connection_handler=db_connection_handler_factory()
        )  # instancia seu repo real
        rt_repo = RefreshTokenRepository(
            db_connection_handler=db_connection_handler_factory()
        )
        create_user_uc = CreateUser(repo)
        create_refresh_token = CreateRefreshToken(rt_repo)

        create_user_uc.create(
            cpf=cpf_vo,
            email=email_vo,
            role=role_vo,
            password=password_vo,
            name=args.name
        )
        create_refresh_token.create(cpf=cpf_vo)
        print("Admin criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar admin: {e}")

if __name__ == "__main__":
    main()
#pylint:disable=all
import pytest
from sqlalchemy import text
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import dotenv
import os

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Este hook é chamado após todos os testes serem executados.
    Aqui, você pode colocar o código de limpeza do banco de dados.
    """
    dotenv.load_dotenv()
    database = os.getenv('TDATABASE')
    if database == 'mysql':
        db_connection_handler = DBConnectionHandler(StringConnection())
        print("Tentando conectar ao banco de dados...")
        with db_connection_handler as db:
            print("Conectado ao banco de dados.")
            try:
                # Desabilitar as restrições de chave estrangeira no MySQL
                db.session.execute(text('SET foreign_key_checks = 0;'))
                print("Restrições de chave estrangeira desabilitadas.")
                
                # Obter todas as tabelas do banco de dados
                result = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()"))
                tables = result.fetchall()

                for table in tables:
                    table_name = table[0]
                    if table_name != 'alembic_version':
                        print(f"Limpando a tabela: {table_name}")
                        db.session.execute(text(f"DELETE FROM {table_name}"))
                
                db.session.commit()
                print("Banco de dados limpo e commit realizado.")

                # Habilitar as restrições de chave estrangeira novamente
                db.session.execute(text('SET foreign_key_checks = 1;'))
                print("Restrições de chave estrangeira reabilitadas.")
            
            except Exception as e:
                print(f"Erro durante o processo de limpeza: {e}")
            finally:
                print("Banco de dados limpo após todos os testes.")


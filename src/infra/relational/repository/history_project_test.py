from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from sqlalchemy import text, TextClause
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime, timezone
import pytest

@pytest.fixture
def monetary_value() -> MonetaryValue:
    return MonetaryValue(10_000)

@pytest.fixture
def andamento_do_projeto() -> str:
    return 'Fase de Protótipo'

@pytest.fixture
def datetime_fixture() -> datetime:
    return datetime.now(timezone.utc)

@pytest.fixture
def insert_project_script() -> TextClause:
    return text('''
    insert into project (status_id, verba_disponivel, andamento_do_projeto, start_date, expected_completion_date, end_date) VALUES (:status_id, :verba_disponivel, :andamento_do_projeto, :start_date, :expected_completion_date, :end_date)
    ''')

@pytest.fixture
def select_project_script() -> TextClause:
    return text('''
    select * from project where status_id = :status_id
    ''')

@pytest.fixture
def insert_status_script() -> TextClause:
    return text('''INSERT INTO status (description, created_at) VALUES (:description, :created_at)''')

@pytest.fixture
def select_status_script() -> TextClause:
    return text('SELECT * FROM status')

@pytest.fixture
def select_history_project() -> TextClause:
    return text('SELECT * from history_project')

@pytest.fixture
def insert_history_project() -> TextClause:
    return text('''
    INSERT INTO history_project (project_id, data_name, description, updated_at) VALUES (:project_id, :data_name, :description, :updated_at)
    ''')

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

def test_insert(
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script,
    select_history_project,
    andamento_do_projeto,
    datetime_fixture
) -> None:
    db_handler = DBConnectionHandler(StringConnection())

    with db_handler as db:
        # Inserindo status
        db.session.execute(
            insert_status_script,
            {"description": "Em Andamento", "created_at": datetime_fixture}
        )
        db.session.commit()

        # Selecionando status
        status_result = db.session.execute(select_status_script).fetchone()
        assert status_result is not None
        status_id = status_result.id

        # Inserindo projeto
        db.session.execute(
            insert_project_script,
            {
                "status_id": status_id,
                "verba_disponivel": 10000.0,
                "andamento_do_projeto": andamento_do_projeto,
                "start_date": datetime_fixture,
                "expected_completion_date": datetime_fixture,
                "end_date": None
            }
        )
        db.session.commit()

        # Selecionando projeto
        project_result = db.session.execute(select_project_script, {"status_id": status_id}).fetchone()
        assert project_result is not None
        project_id = project_result.id

        # Inserindo histórico do projeto via repositório
        repo = HistoryProjectRepository(db_handler)
        repo.insert(
            project_id=project_id,
            data_name="andamento_do_projeto",
            description="Alterado para fase de protótipo"
        )

        # Verificando se foi inserido no banco
        history_result = db.session.execute(select_history_project).fetchall()
        assert len(history_result) == 1
        inserted = history_result[0]
        assert inserted.project_id == project_id
        assert inserted.data_name == "andamento_do_projeto"
        assert inserted.description == "Alterado para fase de protótipo"

def test_find(
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script,
    insert_history_project,
    andamento_do_projeto,
    datetime_fixture
) -> None:
    db_handler = DBConnectionHandler(StringConnection())

    with db_handler as db:
        # Inserindo status
        db.session.execute(
            insert_status_script,
            {"description": "Em Andamento", "created_at": datetime_fixture}
        )
        db.session.commit()

        status_result = db.session.execute(select_status_script).fetchone()
        assert status_result is not None
        status_id = status_result.id

        # Inserindo projeto
        db.session.execute(
            insert_project_script,
            {
                "status_id": status_id,
                "verba_disponivel": 10000.0,
                "andamento_do_projeto": andamento_do_projeto,
                "start_date": datetime_fixture,
                "expected_completion_date": datetime_fixture,
                "end_date": None
            }
        )
        db.session.commit()

        project_result = db.session.execute(select_project_script, {"status_id": status_id}).fetchone()
        assert project_result is not None
        project_id = project_result.id

        # Inserindo histórico diretamente via SQL
        db.session.execute(
            insert_history_project,
            {
                "project_id": project_id,
                "data_name": "andamento_do_projeto",
                "description": "Alterado para fase de protótipo",
                "updated_at": datetime_fixture
            }
        )
        db.session.commit()

        # Recuperando ID do history_project inserido
        history_project_id = db.session.execute(text("SELECT id FROM history_project")).fetchone().id

        # Usando o repositório para buscar o histórico
        repo = HistoryProjectRepository(db_handler)
        result = repo.find(history_project_id)

        assert result is not None
        assert result.history_project_id == history_project_id
        assert result.project_id == project_id
        assert result.data_name == "andamento_do_projeto"
        assert result.description == "Alterado para fase de protótipo"
        assert isinstance(result.updated_at, datetime)

def test_find_all_from_project(
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script,
    insert_history_project,
    andamento_do_projeto,
    datetime_fixture
) -> None:
    db_handler = DBConnectionHandler(StringConnection())

    with db_handler as db:
        # Inserindo status
        db.session.execute(
            insert_status_script,
            {"description": "Em Andamento", "created_at": datetime_fixture}
        )
        db.session.commit()

        status_result = db.session.execute(select_status_script).fetchone()
        assert status_result is not None
        status_id = status_result.id

        # Inserindo projeto
        db.session.execute(
            insert_project_script,
            {
                "status_id": status_id,
                "verba_disponivel": 10000.0,
                "andamento_do_projeto": andamento_do_projeto,
                "start_date": datetime_fixture,
                "expected_completion_date": datetime_fixture,
                "end_date": None
            }
        )
        db.session.commit()

        project_result = db.session.execute(select_project_script, {"status_id": status_id}).fetchone()
        assert project_result is not None
        project_id = project_result.id

        # Inserindo múltiplos históricos para o mesmo projeto
        db.session.execute(
            insert_history_project,
            {
                "project_id": project_id,
                "data_name": "andamento_do_projeto",
                "description": "Alterado para fase de protótipo",
                "updated_at": datetime_fixture
            }
        )
        db.session.execute(
            insert_history_project,
            {
                "project_id": project_id,
                "data_name": "verba_disponivel",
                "description": "Ajuste de orçamento",
                "updated_at": datetime_fixture
            }
        )
        db.session.commit()

        # Testando o método do repositório
        repo = HistoryProjectRepository(db_handler)
        results = repo.find_all_from_project(project_id)

        assert isinstance(results, list)
        assert len(results) == 2

        data_names = [r.data_name for r in results]
        descriptions = [r.description for r in results]

        assert "andamento_do_projeto" in data_names
        assert "verba_disponivel" in data_names
        assert "Alterado para fase de protótipo" in descriptions
        assert "Ajuste de orçamento" in descriptions

def test_update(
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script,
    insert_history_project,
    andamento_do_projeto,
    datetime_fixture
) -> None:
    db_handler = DBConnectionHandler(StringConnection())

    with db_handler as db:
        # Inserindo status
        db.session.execute(
            insert_status_script,
            {"description": "Em Andamento", "created_at": datetime_fixture}
        )
        db.session.commit()

        status_result = db.session.execute(select_status_script).fetchone()
        assert status_result is not None
        status_id = status_result.id

        # Inserindo projeto
        db.session.execute(
            insert_project_script,
            {
                "status_id": status_id,
                "verba_disponivel": 10000.0,
                "andamento_do_projeto": andamento_do_projeto,
                "start_date": datetime_fixture,
                "expected_completion_date": datetime_fixture,
                "end_date": None
            }
        )
        db.session.commit()

        project_result = db.session.execute(select_project_script, {"status_id": status_id}).fetchone()
        assert project_result is not None
        project_id = project_result.id

        # Inserindo histórico
        db.session.execute(
            insert_history_project,
            {
                "project_id": project_id,
                "data_name": "verba_disponivel",
                "description": "Valor inicial",
                "updated_at": datetime_fixture
            }
        )
        db.session.commit()

        # Buscando ID do histórico inserido
        history_project_id = db.session.execute(
            text("SELECT id FROM history_project")
        ).fetchone().id

        # Atualizando o registro com o repositório
        repo = HistoryProjectRepository(db_handler)
        new_description = "Orçamento ajustado para nova etapa"
        repo.update(
            history_project_id,
            {"description": new_description}
        )

        # Verificando atualização no banco
        updated_history = db.session.execute(
            text("SELECT * FROM history_project WHERE id = :id"),
            {"id": history_project_id}
        ).fetchone()

        assert updated_history is not None
        assert updated_history.description == new_description

def test_delete(
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script,
    andamento_do_projeto,
    datetime_fixture
) -> None:
    db_handler = DBConnectionHandler(StringConnection())

    with db_handler as db:
        # Inserindo status
        db.session.execute(
            insert_status_script,
            {"description": "Em Andamento", "created_at": datetime_fixture}
        )
        db.session.commit()

        status_result = db.session.execute(select_status_script).fetchone()
        assert status_result is not None
        status_id = status_result.id

        # Inserindo projeto
        db.session.execute(
            insert_project_script,
            {
                "status_id": status_id,
                "verba_disponivel": 10000.0,
                "andamento_do_projeto": andamento_do_projeto,
                "start_date": datetime_fixture,
                "expected_completion_date": datetime_fixture,
                "end_date": None
            }
        )
        db.session.commit()

        project_result = db.session.execute(select_project_script, {"status_id": status_id}).fetchone()
        assert project_result is not None
        project_id = project_result.id

        # Inserindo histórico via repositório
        repo = HistoryProjectRepository(db_handler)
        repo.insert(
            project_id=project_id,
            data_name="andamento_do_projeto",
            description="Alterado para fase de protótipo"
        )

        # Verificando inserção
        inserted = db.session.execute(text("SELECT id FROM history_project")).fetchone()
        assert inserted is not None
        history_project_id = inserted.id

        # Deletando com o repositório
        repo.delete(history_project_id)

        # Verificando deleção
        result = db.session.execute(text("SELECT * FROM history_project WHERE id = :id"), {"id": history_project_id}).fetchone()
        assert result is None

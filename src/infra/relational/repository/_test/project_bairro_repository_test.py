import pytest
from sqlalchemy import text
from datetime import datetime, timezone
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection
from src.errors.repository.project_bairro_already_exists import ProjectBairroAlreadyExists
from src.errors.repository.projects_from_bairro_does_not_exists import ProjectsFromBairroDoesNotExists

@pytest.fixture(autouse=True)
def cleanup_tables():
    db = DBConnectionHandler(TStringConnection())
    with db as conn:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        conn.session.execute(text('DELETE FROM project_bairro'))
        conn.session.execute(text('DELETE FROM bairro'))
        conn.session.execute(text('DELETE FROM project'))
        conn.session.execute(text('DELETE FROM status'))
        conn.session.commit()


@pytest.fixture
def setup_project_and_bairro():
    db = DBConnectionHandler(TStringConnection())
    with db as conn:
        conn.session.execute(
            text("INSERT INTO status (description, created_at) VALUES (:desc, :created_at)"),
            {"desc": "Ativo", "created_at": datetime.now(timezone.utc)}
        )
        status_id = conn.session.execute(
            text("SELECT id FROM status WHERE description = :desc"),
            {"desc": "Ativo"}
        ).scalar()

        conn.session.execute(
            text('''
                INSERT INTO project (status_id, verba_disponivel, andamento_do_projeto, start_date, expected_completion_date, end_date)
                VALUES (:status_id, 1000, :dt, :dt, :dt, :dt)
            '''), {"status_id": status_id, "dt": datetime.now(timezone.utc)}
        )

        project_id = conn.session.execute(text("SELECT id FROM project")).scalar()

        conn.session.execute(
            text("INSERT INTO bairro (name, created_at) VALUES (:name, :dt)"),
            {"name": "Centro", "dt": datetime.now(timezone.utc)}
        )

        bairro_id = conn.session.execute(text("SELECT id FROM bairro WHERE name = 'Centro'")).scalar()

        conn.session.commit()

        return {"project_id": project_id, "bairro_id": bairro_id}


def test_insert_and_duplicate(setup_project_and_bairro):
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    project_id = setup_project_and_bairro["project_id"]
    bairro_id = setup_project_and_bairro["bairro_id"]

    # Primeira inserção deve passar
    repo.insert(project_id, bairro_id)

    # Segunda inserção deve lançar exceção
    with pytest.raises(ProjectBairroAlreadyExists):
        repo.insert(project_id, bairro_id)


def test_find(setup_project_and_bairro):
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    project_id = setup_project_and_bairro["project_id"]
    bairro_id = setup_project_and_bairro["bairro_id"]

    repo.insert(project_id, bairro_id)

    result = repo.find(project_id, bairro_id)

    assert result.project_id == project_id
    assert result.bairro_id == bairro_id
    assert result.created_at is not None


def test_find_should_fail_for_non_existing():
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    with pytest.raises(ProjectsFromBairroDoesNotExists):
        repo.find(999, 999)


def test_find_all_from_bairro(setup_project_and_bairro):
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    project_id = setup_project_and_bairro["project_id"]
    bairro_id = setup_project_and_bairro["bairro_id"]

    repo.insert(project_id, bairro_id)

    results = repo.find_all_from_bairro(bairro_id)

    assert len(results) == 1
    assert results[0].project_id == project_id


def test_find_all_should_fail_for_empty():
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    with pytest.raises(ProjectsFromBairroDoesNotExists):
        repo.find_all_from_bairro(123456)


def test_update_bairro(setup_project_and_bairro):
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    project_id = setup_project_and_bairro["project_id"]
    bairro_id = setup_project_and_bairro["bairro_id"]

    # Criar novo bairro para atualização
    with db_handler as db:
        db.session.execute(
            text("INSERT INTO bairro (name, created_at) VALUES (:name, :dt)"),
            {"name": "Nova Esperança", "dt": datetime.now(timezone.utc)}
        )
        new_bairro_id = db.session.execute(
            text("SELECT id FROM bairro WHERE name = 'Nova Esperança'")
        ).scalar()
        db.session.commit()

    repo.insert(project_id, bairro_id)

    repo.update_bairro(project_id, bairro_id, new_bairro_id)

    updated = repo.find(project_id, new_bairro_id)
    assert updated.project_id == project_id
    assert updated.bairro_id == new_bairro_id


def test_delete_project_bairro(setup_project_and_bairro):
    db_handler = DBConnectionHandler(TStringConnection())
    repo = ProjectBairroRepository(db_handler)

    project_id = setup_project_and_bairro["project_id"]
    bairro_id = setup_project_and_bairro["bairro_id"]

    repo.insert(project_id, bairro_id)

    repo.delete(project_id, bairro_id)

    with pytest.raises(ProjectsFromBairroDoesNotExists):
        repo.find(project_id, bairro_id)
#pylint:disable=all
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timezone

from src.infra.relational.repository.project_folder_repository import ProjectFolderRepository
from src.domain.entities.project_folder import ProjectFolderEntity
from src.errors.repository.already_exists_error.project_folder_already_exists import ProjectFolderAlreadyExists
from src.errors.repository.not_exists_error.project_folder_not_exists import ProjectFolderNotExists
from src.errors.repository.error_on_insert.error_on_insert_project_folder import ErrorOnInsertProjectFolder
from src.errors.repository.error_on_find.error_on_find_project_folder import ErrorOnFindProjectFolder
from src.errors.repository.error_on_delete.error_on_delete_project_folder import ErrorOnDeleteProjectFolder
from sqlalchemy.exc import IntegrityError


class TestProjectFolderRepository:
    
    @pytest.fixture
    def mock_db_connection_handler(self):
        """Fixture para criar um mock do db_connection_handler"""
        mock_handler = Mock()
        mock_db_context = Mock()
        mock_session = Mock()
        mock_db_context.session = mock_session
        mock_handler.__enter__ = Mock(return_value=mock_db_context)
        mock_handler.__exit__ = Mock(return_value=None)
        return mock_handler
    
    @pytest.fixture
    def project_folder_repository(self, mock_db_connection_handler):
        """Fixture para criar uma instância do ProjectFolderRepository com mock"""
        return ProjectFolderRepository(mock_db_connection_handler)
    
    @pytest.fixture
    def mock_project_folder_model(self):
        """Fixture para criar um mock do modelo ProjectFolder"""
        mock_project_folder = Mock()
        mock_project_folder.id = 1
        mock_project_folder.project_id = 10
        mock_project_folder.folder_id = 20
        mock_project_folder.created_at = datetime.now(timezone.utc)
        mock_project_folder.updated_at = datetime.now(timezone.utc)
        return mock_project_folder
    
    @patch('src.infra.relational.repository.project_folder_repository.ProjectFolder')
    def test_insert_success(self, mock_project_folder_class, project_folder_repository, mock_db_connection_handler):
        """Testa inserção bem-sucedida de associação projeto-pasta"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None  # Não existe associação
        mock_session.query.return_value = mock_query
        mock_project_folder_instance = Mock()
        mock_project_folder_instance.project_id = 10
        mock_project_folder_instance.folder_id = 20
        mock_project_folder_class.return_value = mock_project_folder_instance
        
        # Act
        project_folder_repository.insert(project_id=10, folder_id=20)
        
        # Assert
        mock_project_folder_class.assert_called_once_with(project_id=10, folder_id=20)
        mock_session.add.assert_called_once_with(mock_project_folder_instance)
        mock_session.commit.assert_called_once()
        # Verifica que foi criado com os IDs corretos (inteiros)
        assert mock_project_folder_instance.project_id == 10
        assert mock_project_folder_instance.folder_id == 20
        assert isinstance(mock_project_folder_instance.project_id, int)
        assert isinstance(mock_project_folder_instance.folder_id, int)
    
    def test_insert_duplicate(self, project_folder_repository, mock_db_connection_handler):
        """Testa inserção de associação duplicada"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_existing = Mock()
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = mock_existing  # Já existe
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderAlreadyExists):
            project_folder_repository.insert(project_id=10, folder_id=20)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
    
    @patch('src.infra.relational.repository.project_folder_repository.ProjectFolder')
    def test_insert_integrity_error(self, mock_project_folder_class, project_folder_repository, mock_db_connection_handler):
        """Testa tratamento de IntegrityError na inserção"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        mock_project_folder_instance = Mock()
        mock_project_folder_class.return_value = mock_project_folder_instance
        mock_session.add.side_effect = IntegrityError("", "", "")
        
        # Act & Assert
        with pytest.raises(ProjectFolderAlreadyExists):
            project_folder_repository.insert(project_id=10, folder_id=20)
    
    def test_insert_generic_error(self, project_folder_repository, mock_db_connection_handler):
        """Testa tratamento de erro genérico na inserção"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.side_effect = Exception("Database error")
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ErrorOnInsertProjectFolder):
            project_folder_repository.insert(project_id=10, folder_id=20)
    
    def test_find_success(self, project_folder_repository, mock_db_connection_handler, mock_project_folder_model):
        """Testa busca bem-sucedida de associação"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = mock_project_folder_model
        mock_session.query.return_value = mock_query
        
        # Act
        result = project_folder_repository.find(project_id=10, folder_id=20)
        
        # Assert
        assert isinstance(result, ProjectFolderEntity)
        assert result.id == 1
        assert result.project_id == 10
        assert result.folder_id == 20
        assert isinstance(result.id, int)
        assert isinstance(result.project_id, int)
        assert isinstance(result.folder_id, int)
    
    def test_find_not_found(self, project_folder_repository, mock_db_connection_handler):
        """Testa busca quando associação não existe"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderNotExists):
            project_folder_repository.find(project_id=999, folder_id=999)
    
    def test_find_all_from_folder_success(self, project_folder_repository, mock_db_connection_handler):
        """Testa busca de todos os projetos de uma pasta"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_project_folder1 = Mock()
        mock_project_folder1.id = 1
        mock_project_folder1.project_id = 10
        mock_project_folder1.folder_id = 20
        mock_project_folder1.created_at = datetime.now(timezone.utc)
        mock_project_folder1.updated_at = datetime.now(timezone.utc)
        
        mock_project_folder2 = Mock()
        mock_project_folder2.id = 2
        mock_project_folder2.project_id = 11
        mock_project_folder2.folder_id = 20
        mock_project_folder2.created_at = datetime.now(timezone.utc)
        mock_project_folder2.updated_at = datetime.now(timezone.utc)
        
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = [mock_project_folder1, mock_project_folder2]
        mock_session.query.return_value = mock_query
        
        # Act
        result = project_folder_repository.find_all_from_folder(folder_id=20)
        
        # Assert
        assert len(result) == 2
        assert all(isinstance(pf.id, int) for pf in result)
        assert all(isinstance(pf.folder_id, int) for pf in result)
        assert all(pf.folder_id == 20 for pf in result)
        assert result[0].project_id == 10
        assert result[1].project_id == 11
    
    def test_find_all_from_folder_not_found(self, project_folder_repository, mock_db_connection_handler):
        """Testa busca quando não há projetos para a pasta"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = []
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderNotExists):
            project_folder_repository.find_all_from_folder(folder_id=999)
    
    def test_find_all_from_project_success(self, project_folder_repository, mock_db_connection_handler):
        """Testa busca de todas as pastas de um projeto"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_project_folder1 = Mock()
        mock_project_folder1.id = 1
        mock_project_folder1.project_id = 10
        mock_project_folder1.folder_id = 20
        mock_project_folder1.created_at = datetime.now(timezone.utc)
        mock_project_folder1.updated_at = datetime.now(timezone.utc)
        
        mock_project_folder2 = Mock()
        mock_project_folder2.id = 2
        mock_project_folder2.project_id = 10
        mock_project_folder2.folder_id = 21
        mock_project_folder2.created_at = datetime.now(timezone.utc)
        mock_project_folder2.updated_at = datetime.now(timezone.utc)
        
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = [mock_project_folder1, mock_project_folder2]
        mock_session.query.return_value = mock_query
        
        # Act
        result = project_folder_repository.find_all_from_project(project_id=10)
        
        # Assert
        assert len(result) == 2
        assert all(isinstance(pf.id, int) for pf in result)
        assert all(isinstance(pf.project_id, int) for pf in result)
        assert all(pf.project_id == 10 for pf in result)
        assert result[0].folder_id == 20
        assert result[1].folder_id == 21
    
    def test_find_all_from_project_not_found(self, project_folder_repository, mock_db_connection_handler):
        """Testa busca quando não há pastas para o projeto"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = []
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderNotExists):
            project_folder_repository.find_all_from_project(project_id=999)
    
    def test_delete_success(self, project_folder_repository, mock_db_connection_handler):
        """Testa deleção bem-sucedida de associação"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_project_folder = Mock()
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = mock_project_folder
        mock_query.where.return_value.delete = Mock()
        mock_session.query.return_value = mock_query
        
        # Act
        project_folder_repository.delete(project_id=10, folder_id=20)
        
        # Assert
        mock_query.where.return_value.delete.assert_called_once()
        mock_session.commit.assert_called_once()
    
    def test_delete_not_found(self, project_folder_repository, mock_db_connection_handler):
        """Testa deleção quando associação não existe"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderNotExists):
            project_folder_repository.delete(project_id=999, folder_id=999)
    
    def test_delete_all_from_project_success(self, project_folder_repository, mock_db_connection_handler):
        """Testa deleção de todas as associações de um projeto"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_project_folder = Mock()
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = [mock_project_folder]
        mock_query.where.return_value.delete = Mock()
        mock_session.query.return_value = mock_query
        
        # Act
        project_folder_repository.delete_all_from_project(project_id=10)
        
        # Assert
        mock_query.where.return_value.delete.assert_called_once()
        mock_session.commit.assert_called_once()
    
    def test_delete_all_from_project_not_found(self, project_folder_repository, mock_db_connection_handler):
        """Testa deleção quando não há associações para o projeto"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = []
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderNotExists):
            project_folder_repository.delete_all_from_project(project_id=999)
    
    def test_delete_all_from_folder_success(self, project_folder_repository, mock_db_connection_handler):
        """Testa deleção de todas as associações de uma pasta"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_project_folder = Mock()
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = [mock_project_folder]
        mock_query.where.return_value.delete = Mock()
        mock_session.query.return_value = mock_query
        
        # Act
        project_folder_repository.delete_all_from_folder(folder_id=20)
        
        # Assert
        mock_query.where.return_value.delete.assert_called_once()
        mock_session.commit.assert_called_once()
    
    def test_delete_all_from_folder_not_found(self, project_folder_repository, mock_db_connection_handler):
        """Testa deleção quando não há associações para a pasta"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.all.return_value = []
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(ProjectFolderNotExists):
            project_folder_repository.delete_all_from_folder(folder_id=999)


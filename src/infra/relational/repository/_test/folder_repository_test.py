#pylint:disable=all
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timezone

from src.infra.relational.repository.folder_repository import FolderRepository
from src.domain.entities.folder import FolderEntity
from src.errors.repository.already_exists_error.folder_already_exists import FolderAlreadyExists
from src.errors.repository.not_exists_error.folder_not_exists import FolderNotExists
from src.errors.repository.error_on_insert.error_on_insert_folder import ErrorOnInsertFolder
from src.errors.repository.error_on_find.error_on_find_folder import ErrorOnFindFolder
from src.errors.repository.error_on_update.error_on_update_folder import ErrorOnUpdateFolder
from src.errors.repository.error_on_delete.error_on_delete_folder import ErrorOnDeleteFolder
from src.errors.repository.has_related_children.folder_has_related_children import FolderHasRelatedChildren
from sqlalchemy.exc import IntegrityError


class TestFolderRepository:
    
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
    def folder_repository(self, mock_db_connection_handler):
        """Fixture para criar uma instância do FolderRepository com mock"""
        return FolderRepository(mock_db_connection_handler)
    
    @pytest.fixture
    def mock_folder_model(self):
        """Fixture para criar um mock do modelo Folder"""
        mock_folder = Mock()
        mock_folder.id = 1
        mock_folder.name = "Test Folder"
        mock_folder.created_at = datetime.now(timezone.utc)
        mock_folder.updated_at = datetime.now(timezone.utc)
        return mock_folder
    
    @patch('src.infra.relational.repository.folder_repository.Folder')
    def test_insert_success(self, mock_folder_class, folder_repository, mock_db_connection_handler):
        """Testa inserção bem-sucedida de uma pasta"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None  # Não existe pasta com esse nome
        mock_session.query.return_value = mock_query
        mock_folder_instance = Mock()
        mock_folder_class.return_value = mock_folder_instance
        
        # Act
        folder_repository.insert("Test Folder")
        
        # Assert
        mock_folder_class.assert_called_once_with(name="Test Folder")
        mock_session.add.assert_called_once_with(mock_folder_instance)
        mock_session.commit.assert_called_once()
    
    def test_insert_duplicate_name(self, folder_repository, mock_db_connection_handler):
        """Testa inserção de pasta com nome duplicado"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_existing_folder = Mock()
        mock_query.where.return_value.first.return_value = mock_existing_folder  # Já existe
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(FolderAlreadyExists):
            folder_repository.insert("Test Folder")
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
    
    def test_insert_error(self, folder_repository, mock_db_connection_handler):
        """Testa tratamento de erro genérico na inserção"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        # Simula erro ao fazer query
        mock_session.query.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(ErrorOnInsertFolder):
            folder_repository.insert("Test Folder")
    
    def test_find_by_id_success(self, folder_repository, mock_db_connection_handler, mock_folder_model):
        """Testa busca por ID bem-sucedida"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = mock_folder_model
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.find_by_id(1)
        
        # Assert
        assert isinstance(result, FolderEntity)
        assert result.folder_id == 1
        assert result.name == "Test Folder"
        assert isinstance(result.folder_id, int)
    
    def test_find_by_id_not_found(self, folder_repository, mock_db_connection_handler):
        """Testa busca por ID quando não encontra"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(FolderNotExists):
            folder_repository.find_by_id(999)
    
    def test_find_by_name_success(self, folder_repository, mock_db_connection_handler, mock_folder_model):
        """Testa busca por nome bem-sucedida"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = mock_folder_model
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.find_by_name("Test Folder")
        
        # Assert
        assert result is not None
        assert isinstance(result, FolderEntity)
        assert result.name == "Test Folder"
        assert isinstance(result.folder_id, int)
    
    def test_find_by_name_not_found(self, folder_repository, mock_db_connection_handler):
        """Testa busca por nome quando não encontra"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.find_by_name("Non Existent")
        
        # Assert
        assert result is None
    
    def test_find_all_success(self, folder_repository, mock_db_connection_handler):
        """Testa busca de todas as pastas"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_folder1 = Mock()
        mock_folder1.id = 1
        mock_folder1.name = "Folder 1"
        mock_folder1.created_at = datetime.now(timezone.utc)
        mock_folder1.updated_at = datetime.now(timezone.utc)
        
        mock_folder2 = Mock()
        mock_folder2.id = 2
        mock_folder2.name = "Folder 2"
        mock_folder2.created_at = datetime.now(timezone.utc)
        mock_folder2.updated_at = datetime.now(timezone.utc)
        
        mock_query = Mock()
        mock_query.all.return_value = [mock_folder1, mock_folder2]
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.find_all()
        
        # Assert
        assert len(result) == 2
        assert all(isinstance(f.folder_id, int) for f in result)
        assert result[0].name == "Folder 1"
        assert result[1].name == "Folder 2"
    
    def test_update_success(self, folder_repository, mock_db_connection_handler):
        """Testa atualização bem-sucedida"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_folder = Mock()
        mock_query = Mock()
        mock_query_where = Mock()
        mock_query_where.first.return_value = mock_folder
        mock_query_where.update = Mock()
        mock_query.where.return_value = mock_query_where
        mock_session.query.return_value = mock_query
        
        # Act
        folder_repository.update(1, "New Name")
        
        # Assert
        mock_query_where.update.assert_called_once_with({'name': 'New Name'})
        mock_session.commit.assert_called_once()
    
    def test_update_not_found(self, folder_repository, mock_db_connection_handler):
        """Testa atualização quando pasta não existe"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(FolderNotExists):
            folder_repository.update(999, "New Name")
    
    def test_delete_success(self, folder_repository, mock_db_connection_handler):
        """Testa deleção bem-sucedida"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_folder = Mock()
        mock_query = Mock()
        mock_query_where = Mock()
        mock_query_where.first.return_value = mock_folder
        mock_query_where.delete = Mock()
        mock_query.where.return_value = mock_query_where
        mock_session.query.return_value = mock_query
        
        # Act
        folder_repository.delete(1)
        
        # Assert
        mock_query_where.delete.assert_called_once()
        mock_session.commit.assert_called_once()
    
    def test_delete_not_found(self, folder_repository, mock_db_connection_handler):
        """Testa deleção quando pasta não existe"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.where.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(FolderNotExists):
            folder_repository.delete(999)
    
    def test_delete_with_related_children(self, folder_repository, mock_db_connection_handler):
        """Testa deleção quando pasta tem relacionamentos"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_folder = Mock()
        mock_query = Mock()
        mock_query_where = Mock()
        mock_query_where.first.return_value = mock_folder
        mock_query_where.delete.side_effect = IntegrityError("", "", "")
        mock_query.where.return_value = mock_query_where
        mock_session.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(FolderHasRelatedChildren):
            folder_repository.delete(1)
    
    def test_find_all_with_pagination(self, folder_repository, mock_db_connection_handler):
        """Testa busca com paginação"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_folder = Mock()
        mock_folder.id = 1
        mock_folder.name = "Folder 1"
        mock_folder.created_at = datetime.now(timezone.utc)
        mock_folder.updated_at = datetime.now(timezone.utc)
        
        mock_query = Mock()
        mock_offset = Mock()
        mock_limit = Mock()
        mock_limit.all.return_value = [mock_folder]
        mock_offset.limit.return_value = mock_limit
        mock_query.offset.return_value = mock_offset
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.find_all_with_pagination(page_size=10, page=1)
        
        # Assert
        assert len(result) == 1
        assert isinstance(result[0].folder_id, int)
        mock_query.offset.assert_called_once_with(0)
        mock_offset.limit.assert_called_once_with(10)
    
    def test_count_all(self, folder_repository, mock_db_connection_handler):
        """Testa contagem de todas as pastas"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_query.count.return_value = 5
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.count_all()
        
        # Assert
        assert result == 5
    
    def test_find_all_with_pagination_and_filter(self, folder_repository, mock_db_connection_handler):
        """Testa busca com paginação e filtro"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_folder = Mock()
        mock_folder.id = 1
        mock_folder.name = "Test Folder"
        mock_folder.created_at = datetime.now(timezone.utc)
        mock_folder.updated_at = datetime.now(timezone.utc)
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_offset = Mock()
        mock_limit = Mock()
        mock_limit.all.return_value = [mock_folder]
        mock_offset.limit.return_value = mock_limit
        mock_filter.offset.return_value = mock_offset
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.find_all_with_pagination_and_filter(
            page_size=10, page=1, search_term="Test"
        )
        
        # Assert
        assert len(result) == 1
        assert result[0].name == "Test Folder"
        assert isinstance(result[0].folder_id, int)
        mock_query.filter.assert_called_once()
    
    def test_count_all_with_filter(self, folder_repository, mock_db_connection_handler):
        """Testa contagem com filtro"""
        # Arrange
        mock_db_context = mock_db_connection_handler.__enter__.return_value
        mock_session = mock_db_context.session
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.count.return_value = 3
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query
        
        # Act
        result = folder_repository.count_all_with_filter(search_term="Test")
        
        # Assert
        assert result == 3
        mock_query.filter.assert_called_once()

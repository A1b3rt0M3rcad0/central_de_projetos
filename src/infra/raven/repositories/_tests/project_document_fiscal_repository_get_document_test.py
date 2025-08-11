# pylint: disable=attribute-defined-outside-init,unused-import
import pytest
from unittest.mock import Mock, MagicMock
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.interface.i_db_connection_handler import IDBConnectionHandler

class TestProjectDocumentFiscalRepositoryGetDocument:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_db_connection_handler = Mock(spec=IDBConnectionHandler)
        self.repository = ProjectDocumentFiscalRepository(self.mock_db_connection_handler)
    
    def test_get_document_by_work_project_and_name_success(self):
        """Test successful document retrieval"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.jpg"
        expected_data = b'document_binary_data'
        
        # Mock database context
        mock_db = Mock()
        self.mock_db_connection_handler.__enter__ = Mock(return_value=mock_db)
        self.mock_db_connection_handler.__exit__ = Mock(return_value=None)
        
        # Mock entity loading
        mock_entity = Mock()
        mock_db.load.return_value = mock_entity
        
        # Mock attachment result
        mock_attachment_result = Mock()
        mock_attachment_result.data = expected_data
        mock_db.advanced.attachments.get.return_value = mock_attachment_result
        
        # Act
        result = self.repository.get_document_by_work_project_and_name(
            work_project_id=work_project_id,
            document_name=document_name
        )
        
        # Assert
        assert result == expected_data
        
        # Verify database operations
        mock_db.load.assert_called_once()
        mock_db.advanced.attachments.get.assert_called_once_with(mock_entity, document_name)
    
    def test_get_document_by_work_project_and_name_work_project_not_found(self):
        """Test when work project is not found"""
        # Arrange
        work_project_id = 999
        document_name = "test_document.jpg"
        
        # Mock database context
        mock_db = Mock()
        self.mock_db_connection_handler.__enter__ = Mock(return_value=mock_db)
        self.mock_db_connection_handler.__exit__ = Mock(return_value=None)
        
        # Mock entity loading returns None (work project not found)
        mock_db.load.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match=f"Work project {work_project_id} não encontrado"):
            self.repository.get_document_by_work_project_and_name(
                work_project_id=work_project_id,
                document_name=document_name
            )
        
        # Verify database operations
        mock_db.load.assert_called_once()
        mock_db.advanced.attachments.get.assert_not_called()
    
    def test_get_document_by_work_project_and_name_document_not_found(self):
        """Test when document is not found in work project"""
        # Arrange
        work_project_id = 1
        document_name = "nonexistent_document.jpg"
        
        # Mock database context
        mock_db = Mock()
        self.mock_db_connection_handler.__enter__ = Mock(return_value=mock_db)
        self.mock_db_connection_handler.__exit__ = Mock(return_value=None)
        
        # Mock entity loading
        mock_entity = Mock()
        mock_db.load.return_value = mock_entity
        
        # Mock attachment result returns None (document not found)
        mock_db.advanced.attachments.get.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match=f"Documento {document_name} não encontrado no work project {work_project_id}"):
            self.repository.get_document_by_work_project_and_name(
                work_project_id=work_project_id,
                document_name=document_name
            )
        
        # Verify database operations
        mock_db.load.assert_called_once()
        mock_db.advanced.attachments.get.assert_called_once_with(mock_entity, document_name)
    
    def test_get_document_by_work_project_and_name_different_document_types(self):
        """Test document retrieval with different document types"""
        # Arrange
        test_cases = [
            (1, "image.jpg", b'image_data'),
            (2, "document.pdf", b'pdf_data'),
            (3, "report.docx", b'docx_data'),
            (4, "data.xlsx", b'excel_data'),
            (5, "video.mp4", b'video_data'),
        ]
        
        for work_project_id, document_name, expected_data in test_cases:
            # Mock database context
            mock_db = Mock()
            self.mock_db_connection_handler.__enter__ = Mock(return_value=mock_db)
            self.mock_db_connection_handler.__exit__ = Mock(return_value=None)
            
            # Mock entity loading
            mock_entity = Mock()
            mock_db.load.return_value = mock_entity
            
            # Mock attachment result
            mock_attachment_result = Mock()
            mock_attachment_result.data = expected_data
            mock_db.advanced.attachments.get.return_value = mock_attachment_result
            
            # Act
            result = self.repository.get_document_by_work_project_and_name(
                work_project_id=work_project_id,
                document_name=document_name
            )
            
            # Assert
            assert result == expected_data
            
            # Verify database operations
            mock_db.load.assert_called_once()
            mock_db.advanced.attachments.get.assert_called_once_with(mock_entity, document_name)
    
    def test_get_document_by_work_project_and_name_database_error(self):
        """Test when database operation fails"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.jpg"
        
        # Mock database context to raise exception
        self.mock_db_connection_handler.__enter__ = Mock(side_effect=Exception("Database connection error"))
        self.mock_db_connection_handler.__exit__ = Mock(return_value=None)
        
        # Act & Assert
        with pytest.raises(Exception, match="Database connection error"):
            self.repository.get_document_by_work_project_and_name(
                work_project_id=work_project_id,
                document_name=document_name
            )
    
    def test_get_document_by_work_project_and_name_attachment_error(self):
        """Test when attachment operation fails"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.jpg"
        
        # Mock database context
        mock_db = Mock()
        self.mock_db_connection_handler.__enter__ = Mock(return_value=mock_db)
        self.mock_db_connection_handler.__exit__ = Mock(return_value=None)
        
        # Mock entity loading
        mock_entity = Mock()
        mock_db.load.return_value = mock_entity
        
        # Mock attachment operation to raise exception
        mock_db.advanced.attachments.get.side_effect = Exception("Attachment error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Attachment error"):
            self.repository.get_document_by_work_project_and_name(
                work_project_id=work_project_id,
                document_name=document_name
            )
        
        # Verify database operations
        mock_db.load.assert_called_once()
        mock_db.advanced.attachments.get.assert_called_once_with(mock_entity, document_name) 
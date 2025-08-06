import pytest
from unittest.mock import Mock
from src.data.use_cases.update_work_project_photo import UpdateWorkProjectPhoto
from src.domain.entities.work_project import WorkProjectEntity
from src.errors.use_cases.photo_not_in_documents_error import PhotoNotInDocumentsError

class TestUpdateWorkProjectPhoto:
    
    def test_update_work_project_photo_success(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["projeto_foto.jpg", "outro_doc.pdf"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "projeto_foto.jpg"
        
        # Act
        use_case.update(work_project_id, photo_name)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"photo_name": photo_name}
        )
    
    def test_update_work_project_photo_empty_string_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = ""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Photo name cannot be empty"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_whitespace_only_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "   "
        
        # Act & Assert
        with pytest.raises(ValueError, match="Photo name cannot be empty"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_none_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Photo name cannot be empty"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_invalid_extension_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "documento.pdf"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid file extension. Only image files are allowed"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_valid_extensions_success(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["foto.jpg", "imagem.png", "photo.jpeg", "img.gif", "pic.bmp", "image.webp"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        
        # Testar todas as extensões válidas
        valid_extensions = ["foto.jpg", "imagem.png", "photo.jpeg", "img.gif", "pic.bmp", "image.webp"]
        
        for photo_name in valid_extensions:
            # Act
            use_case.update(work_project_id, photo_name)
            
            # Assert
            mock_repository.find.assert_called_with(work_project_id)
            mock_repository.update.assert_called_with(
                work_project_id=work_project_id,
                update_params={"photo_name": photo_name}
            )
            
            # Reset mocks for next iteration
            mock_repository.find.reset_mock()
            mock_repository.update.reset_mock()
    
    def test_update_work_project_photo_photo_not_in_documents_raises_error(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["doc1.pdf", "doc2.docx"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "foto_inexistente.jpg"
        
        # Act & Assert
        with pytest.raises(PhotoNotInDocumentsError, match="Photo 'foto_inexistente.jpg' must exist in additional_documents before updating work_project photo"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_no_documents_raises_error(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = None
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "foto.jpg"
        
        # Act & Assert
        with pytest.raises(PhotoNotInDocumentsError, match="Photo 'foto.jpg' must exist in additional_documents before updating work_project photo"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_invalid_json_documents_raises_error(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = 'invalid json'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "foto.jpg"
        
        # Act & Assert
        with pytest.raises(PhotoNotInDocumentsError, match="Photo 'foto.jpg' must exist in additional_documents before updating work_project photo"):
            use_case.update(work_project_id, photo_name)
        
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_photo_strips_whitespace(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["foto_projeto.jpg"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectPhoto(mock_repository)
        work_project_id = 1
        photo_name = "  foto_projeto.jpg  "
        
        # Act
        use_case.update(work_project_id, photo_name)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"photo_name": "foto_projeto.jpg"}
        ) 
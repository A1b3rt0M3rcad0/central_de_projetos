#pylint:disable=W0611
import pytest
from src.data.use_cases.save_fiscal_document import SaveFiscalDocument
from src.data.use_cases.get_fiscal_document import GetFiscalDocument
from src.data.use_cases.get_fiscal_document_names import GetFiscalDocumentNames
from src.data.use_cases.delete_fiscal_document import DeleteFiscalDocument
from src.data.use_cases.delete_all_fiscal_documents_from_project import DeleteAllFiscalDocumentsFromProject
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.domain.value_objects.generic_document import GenericDocument
from unittest.mock import Mock

class TestFiscalDocumentIntegration:
    
    def test_fiscal_document_workflow(self):
        """
        Testa o fluxo completo de documentos de fiscais usando mocks simples
        """
        # Arrange
        mock_repository = Mock()
        
        save_use_case = SaveFiscalDocument(mock_repository)
        get_use_case = GetFiscalDocument(mock_repository)
        get_names_use_case = GetFiscalDocumentNames(mock_repository)
        delete_use_case = DeleteFiscalDocument(mock_repository)
        delete_all_use_case = DeleteAllFiscalDocumentsFromProject(mock_repository)
        
        project_id = 123
        fiscal_id = 456
        documents = [
            GenericDocument(document=b"content1", document_name="relatorio.pdf", content_type="application/pdf"),
            GenericDocument(document=b"content2", document_name="foto.jpg", content_type="image/jpeg")
        ]
        
        # Mock das respostas do repositório
        mock_repository.get_fiscal_document_names.return_value = ["relatorio.pdf", "foto.jpg"]
        mock_document = GenericDocument(document=b"content1", document_name="relatorio.pdf", content_type="application/pdf")
        mock_repository.get_fiscal_document.return_value = mock_document
        
        # Act & Assert - 1. Salvar documentos
        save_use_case.save(project_id, fiscal_id, documents)
        mock_repository.insert_fiscal_documents.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id,
            documents=documents
        )
        
        # Act & Assert - 2. Listar nomes dos documentos
        document_names = get_names_use_case.get_names(project_id, fiscal_id)
        assert document_names == ["relatorio.pdf", "foto.jpg"]
        mock_repository.get_fiscal_document_names.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id
        )
        
        # Act & Assert - 3. Obter documento específico
        document = get_use_case.get(project_id, fiscal_id, "relatorio.pdf")
        assert document == mock_document
        mock_repository.get_fiscal_document.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id,
            document_name="relatorio.pdf"
        )
        
        # Act & Assert - 4. Deletar documento específico
        delete_use_case.delete(project_id, fiscal_id, "relatorio.pdf")
        mock_repository.delete_fiscal_document.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id,
            document_name="relatorio.pdf"
        )
        
        # Act & Assert - 5. Deletar todos os documentos
        delete_all_use_case.delete_all(project_id, fiscal_id)
        mock_repository.delete_all_fiscal_documents_from_project.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id
        ) 
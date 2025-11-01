from abc import ABC , abstractmethod
from typing import List , Optional
from app.domain.entities.document import Document

class IDocumentRepositroy(ABC):
    """Repository interface for document operations - the layer 
    between the service and the actual database"""

    @abstractmethod
    async def save(self,document:Document) -> Document:
        """save or update a document"""
        pass

    @abstractmethod
    async def get_by_id(self , document_id:str)->Optional[Document]:
        """Get document by ID"""
        pass

    @abstractmethod
    async def get_by_filename(
        self,
        filename:str,
        user_id:str
    ) -> Optional[Document]:
        """Get document by filename for a specific user"""
        pass 

    @abstractmethod
    async def list_by_user(self,
                           user_id:str ,
                           limit:int = 50 ,
                           offset:int = 0) -> List[Document]: 
        """List documents for a user"""
        pass

    @abstractmethod
    async def delete(self , document_id) -> None:
        """Delete a document"""
        pass

    @abstractmethod
    async def exists(self , document_id:str) -> bool:
        """Check if document exists"""
        pass

    @abstractmethod
    async def count_by_user(self , user_id:str) ->int:
        """Count total documents for a user"""
        pass

    @abstractmethod
    async def search_by_user(self,
                             user_id:str,
                             query:str,
                             limit:int =10) -> List[Document]:
        """Search documents by content for a user"""
        pass

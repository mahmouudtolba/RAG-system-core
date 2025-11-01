from abc import ABC ,abstractmethod
from typing import Optional

class IStorageService(ABC):
    """Interface for file storage operations - Raw PDF bytes"""

    @abstractmethod
    async def upload(self , key:str , content:bytes) -> str:
        """Upload file and return URL"""
        pass

    @abstractmethod
    async def download(self , key:str) -> bytes:
        """Download file content"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete file"""
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        """Get presigned URL for file"""
        pass

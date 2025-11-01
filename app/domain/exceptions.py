class DomainException(Exception):
    """Base exception for domain errors"""
    pass

class DocumentNotFoundError(DomainException):
    pass

class InvalidDocumentFormatError(DomainException):
    pass

class EmbeddingError(DomainException):
    pass

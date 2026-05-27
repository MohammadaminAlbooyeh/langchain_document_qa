class DocumentQAException(Exception):
    pass


class DocumentNotFoundError(DocumentQAException):
    def __init__(self, document_id: str):
        self.document_id = document_id
        super().__init__(f"Document not found: {document_id}")


class UnsupportedFileTypeError(DocumentQAException):
    def __init__(self, file_type: str):
        super().__init__(f"Unsupported file type: {file_type}")


class FileSizeExceededError(DocumentQAException):
    def __init__(self, max_size_mb: int):
        super().__init__(f"File size exceeds maximum of {max_size_mb}MB")


class LLMError(DocumentQAException):
    pass


class VectorStoreError(DocumentQAException):
    pass

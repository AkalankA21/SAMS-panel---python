class SAMSError(Exception):
    # Base Exception
    pass


class ImageValidationError(SAMSError):
    # Image validation failed.
    pass


class ImageLoadingError(SAMSError):
    # Image loading failed.
    pass


class ImageProcessingError(SAMSError):
    # Image processing failed.
    pass


class XMLParsingError(SAMSError):
    # XML parsing failed.
    pass


class DatabaseError(SAMSError):
    # Database operation failed.
    pass


class SignatureDetectionError(SAMSError):
    # Signature detection failed.
    pass
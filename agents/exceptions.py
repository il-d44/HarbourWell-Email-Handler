class EmailClassificationError(Exception):
    """Raised when email classification fails."""
    pass

class EmailClassificationAPIError(EmailClassificationError):
    """Raised when the API call to classify an email fails."""
    pass
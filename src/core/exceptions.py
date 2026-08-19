"""Application exceptions."""


class SoftImoveisError(Exception):
    """Base application error."""


class RepositoryError(SoftImoveisError):
    """Raised when a repository cannot fulfill a request."""


class BusinessRuleUnknownError(SoftImoveisError):
    """Raised when a real business rule has not been discovered yet."""


class UserFacingError(SoftImoveisError):
    """Error that can be summarized safely in the UI."""

    def __init__(self, title: str, message: str) -> None:
        super().__init__(message)
        self.title = title
        self.message = message


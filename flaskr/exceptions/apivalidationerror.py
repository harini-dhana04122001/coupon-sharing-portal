from flaskr.exceptions.apierror import APIError


class APIValidationError(APIError):
    """Custom Authentication Error Class."""
    code = 400
    description = "Validation Error"

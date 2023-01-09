from flaskr.exceptions.apierror import APIError


class ErrorResponse(APIError):
    """Custom Authentication Error Class."""
    code = 400
    description = "Validation Error"

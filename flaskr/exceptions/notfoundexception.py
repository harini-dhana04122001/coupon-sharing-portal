from flaskr.exceptions.apierror import APIError


class NotFoundException(Exception):
    description = "Details not Found"

    def __init__(self, message):
        self.message = message


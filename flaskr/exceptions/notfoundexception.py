class NotFoundException(Exception):
    description = 'Details Not found'

    def __init__(self, message):
        self.message = message


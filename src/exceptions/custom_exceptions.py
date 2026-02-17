
class ConflictException(Exception):
    def __init__(self, message: str, error_code: str = "CONFLICT"):
        self.message = message
        self.error_code = error_code


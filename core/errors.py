class AppError(Exception):
    def __init__(self, message='Internal Server Error', status=500):
        super().__init__(message)
        self.message = message
        self.status = status

class NotFoundError(AppError):
    def __init__(self, message='Not Found'):
        super().__init__(message, 404)

class ConflictError(AppError):
    def __init__(self, message='Conflict'):
        super().__init__(message, 409)

class ValidationError(AppError):
    def __init__(self, message='Validation Error'):
        super().__init__(message, 422)

class UnauthorizedError(AppError):
    def __init__(self, message='Unauthorized'):
        super().__init__(message, 401)

class ForbiddenError(AppError):
    def __init__(self, message='Forbidden'):
        super().__init__(message, 403)

class CameraError(Exception):
    """Base class for all camera-related errors."""


class CommandError(CameraError):
    def __init__(self, message: str, code: int = -1):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


class ConnectionError(CameraError):
    pass


class AuthenticationError(CameraError):
    pass


def handle_errors(error_type=CommandError):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                raise error_type(str(e)) from e

        return wrapper

    return decorator

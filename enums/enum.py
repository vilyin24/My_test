import enum

class StatusCode(enum.Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class ErrorCode(enum.Enum):
    SUCCESS = 0
    CLIENT_NOT_FOUND = 404
    INTERNAL_ERROR = 500

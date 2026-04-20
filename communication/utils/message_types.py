from enum import Enum

class MessageTypes(Enum):
    AUTHORIZATION_REQUEST = '0'
    AUTHORIZATION_ATTEMPT = '1'
    AUTHORIZATION_SUCCESS = '2'
    MESSAGE = '3'
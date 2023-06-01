from ninja_extra import status
from ninja_extra.exceptions import APIException


class ModelNotFoundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Model not found"
    default_code = "bad_request"


class PasswordNotValidException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The password that you entered is not valid.Please use stronger password."



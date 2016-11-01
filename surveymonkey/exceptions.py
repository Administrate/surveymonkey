# -*- coding: utf-8 -*-


class SurveyMonkeyException(Exception):
    def __init__(self, response):
        data = response.json()
        super(SurveyMonkeyException, self).__init__(data["error"]["message"])
        self.status_code = response.status_code
        self.error_code = data["error"]["id"]


class SurveyMonkeyBadRequest(SurveyMonkeyException):
    pass


class SurveyMonkeyAuthorizationError(SurveyMonkeyException):
    pass


class SurveyMonkeyPermissionError(SurveyMonkeyException):
    pass


class SurveyMonkeyResourceNotFound(SurveyMonkeyException):
    pass


class SurveyMonkeyResourceConflict(SurveyMonkeyException):
    pass


class SurveyMonkeyRequestEntityTooLarge(SurveyMonkeyException):
    pass


class SurveyMonkeyInternalServerError(SurveyMonkeyException):
    pass


class SurveyMonkeyUserSoftDeleted(SurveyMonkeyException):
    pass


class SurveyMonkeyUserDeleted(SurveyMonkeyException):
    pass


def response_raises(response):

    def _not_found(response):
        if response.json()["error"]["id"] == "1052":
            return SurveyMonkeyUserSoftDeleted
        else:
            return SurveyMonkeyResourceNotFound

    def _client_error(code):
        return {
            400: SurveyMonkeyBadRequest,
            401: SurveyMonkeyAuthorizationError,
            403: SurveyMonkeyPermissionError,
            409: SurveyMonkeyResourceConflict,
            413: SurveyMonkeyRequestEntityTooLarge,
            410: SurveyMonkeyUserDeleted
        }.get(code)

    def _server_error(code):
        return {
            500: SurveyMonkeyInternalServerError,
            503: SurveyMonkeyInternalServerError
        }.get(code)

    code = response.status_code

    if 200 <= code <= 399:
        return
    elif code == 404:
        exception = _not_found(response)
    elif 400 <= code <= 499:
        exception = _client_error(code)
    elif 500 <= code <= 599:
        exception = _server_error(code)
    else:
        exception = None

    if exception:
        raise exception(response)  # If we don't find a matching status code don't assume failure

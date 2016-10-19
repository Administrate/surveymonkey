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


class SurveyMonkeyPageOutOfRange(Exception):
    def __init__(self):
        super(SurveyMonkeyPageOutOfRange, self).__init__("Requested page is out of range")


def response_raises(response):
    if response.status_code == 200:
        return
    elif response.status_code == 400:
        raise SurveyMonkeyBadRequest(response)
    elif response.status_code == 401:
        raise SurveyMonkeyAuthorizationError(response)
    elif response.status_code == 403:
        raise SurveyMonkeyPermissionError(response)
    elif response.status_code == 404:
        if response.json()["error"]["id"] == "1052":
            raise SurveyMonkeyUserSoftDeleted(response)
        else:
            raise SurveyMonkeyResourceNotFound(response)
    elif response.status_code == 409:
        raise SurveyMonkeyResourceConflict(response)
    elif response.status_code == 413:
        raise SurveyMonkeyRequestEntityTooLarge(response)
    elif response.status_code in [500, 503]:
        raise SurveyMonkeyInternalServerError(response)
    elif response.status_code == 410:
        raise SurveyMonkeyUserDeleted(response)

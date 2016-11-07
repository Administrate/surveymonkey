#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest
from httmock import HTTMock
from expects import expect, contain, equal

from surveymonkey.manager import BaseManager

from surveymonkey.exceptions import (
    SurveyMonkeyBadRequest, SurveyMonkeyAuthorizationError,
    SurveyMonkeyPermissionError, SurveyMonkeyResourceNotFound,
    SurveyMonkeyResourceConflict, SurveyMonkeyRequestEntityTooLarge,
    SurveyMonkeyInternalServerError, SurveyMonkeyUserSoftDeleted,
    SurveyMonkeyUserDeleted
)

from surveymonkey.tests.utils import create_fake_connection
from surveymonkey.tests.mocks.errors import ErrorResponseMocks


class ExceptionFixtures(object):

    def __init__(self):
        self.mocks = ErrorResponseMocks()
        self.possible_exceptions = [
            (
                self.mocks.bad_request,
                SurveyMonkeyBadRequest,
                "Unable to process the request"
            ),
            (
                self.mocks.authorization_error,
                SurveyMonkeyAuthorizationError,
                "The authorization token was not provided"
            ),
            (
                self.mocks.permission_error,
                SurveyMonkeyPermissionError,
                "Permission has not been granted"
            ),
            (
                self.mocks.resource_not_found,
                SurveyMonkeyResourceNotFound,
                "an error retrieving the requested resource"
            ),
            (
                self.mocks.resource_conflict,
                SurveyMonkeyResourceConflict,
                "Unable to complete the request due to a conflict"
            ),
            (
                self.mocks.request_entity_too_large,
                SurveyMonkeyRequestEntityTooLarge,
                "The requested entity is too large"
            ),
            (
                self.mocks.internal_server_error,
                SurveyMonkeyInternalServerError,
                "Oh bananas!"
            ),
            (
                self.mocks.internal_server_error_unreachable,
                SurveyMonkeyInternalServerError,
                "Service unreachable"
            ),
            (
                self.mocks.user_soft_deleted,
                SurveyMonkeyUserSoftDeleted,
                "has been soft deleted"
            ),
            (
                self.mocks.user_deleted,
                SurveyMonkeyUserDeleted,
                "has been deleted"
            ),
        ]


class TestSurveymonkeyExceptions(object):

    def setup_class(self):
        self.mocks = ErrorResponseMocks()
        self.ACCESS_TOKEN, self.connection = create_fake_connection()
        self.manager = BaseManager(self.connection)

    @pytest.mark.parametrize("mock,surveymonkey_exception,error_message", ExceptionFixtures().possible_exceptions)  # noqa:E501
    def test_correct_exception_raised_for_status_code_and_surveymonkey_error_code(self, mock, surveymonkey_exception, error_message):  # noqa:E501
        with HTTMock(mock):
            with pytest.raises(surveymonkey_exception) as e:
                self.manager.get("mocked://")

            expect(str(e.value)).to(contain(error_message))

    def test_exception_includes_survey_monkey_id_and_not_just_http_status_code(self):
        with HTTMock(self.mocks.resource_not_found):
            with pytest.raises(SurveyMonkeyResourceNotFound) as e:
                self.manager.get("mocked://")

            expect(e.value.status_code).to(equal(404))
            expect(e.value.error_code).to(equal("1020"))  # Errorcode from SurveyMonkey are strings

    def test_unknown_status_code_does_not_raise_an_exception(self):
        with HTTMock(self.mocks.not_within_surveymonkey_error_code_range):
            self.manager.get("mocked://")

    def test_2xx_does_not_raise_an_exception(self):
        with HTTMock(self.mocks.status_2xx):
            self.manager.get("mocked://")

    def test_3xx_does_not_raise_an_exception(self):
        with HTTMock(self.mocks.status_3xx):
            self.manager.get("mocked://")

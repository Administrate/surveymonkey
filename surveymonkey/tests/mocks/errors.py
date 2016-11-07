# -*- coding: utf-8 -*-
from __future__ import absolute_import

from httmock import all_requests, response
from surveymonkey.tests.mocks.utils import create_quota_headers


class ErrorResponseMocks(object):

    @staticmethod
    def _create_response(id, status_code, name, message):
        headers = create_quota_headers()
        content = {
            "error": {
                "docs": "https://developer.surveymonkey.com/api/v3/#error-codes",
                "message": message,
                "id": id,
                name: name,
                "http_status_code": status_code
            }
        }

        return response(status_code, content, headers)

    @all_requests
    def bad_request(self, url, request):
        return self._create_response(
            status_code=400,
            id="1000",
            name="Bad Request",
            message="Unable to process the request with the provided input."
        )

    @all_requests
    def authorization_error(self, url, request):
        return self._create_response(
            status_code=401,
            id="1010",
            name="Authorization Error",
            message="The authorization token was not provided."
        )

    @all_requests
    def permission_error(self, url, request):
        return self._create_response(
            status_code=403,
            id="1014",
            name="Permission Error",
            message="Permission has not been granted by the user to make this request."
        )

    @all_requests
    def resource_not_found(self, url, request):
        return self._create_response(
            status_code=404,
            id="1020",
            name="Resource Not Found",
            message="There was an error retrieving the requested resource."
        )

    @all_requests
    def resource_conflict(self, url, request):
        return self._create_response(
            status_code=409,
            id="1025",
            name="Resource Conflict",
            message="Unable to complete the request due to a conflict."
                    "Check the settings for the resource."
        )

    @all_requests
    def request_entity_too_large(self, url, request):
        return self._create_response(
            status_code=413,
            id="1030",
            name="Request Entity Too Large",
            message="The requested entity is too large, it can not be returned."
        )

    @all_requests
    def internal_server_error(self, url, request):
        return self._create_response(
            status_code=500,
            id="1050",
            name="Internal Server Error",
            message="Oh bananas! We couldn't process your request."
        )

    @all_requests
    def internal_server_error_unreachable(self, url, request):
        return self._create_response(
            status_code=503,
            id="1051",
            name="Internal Server Error",
            message="Service unreachable. Please try again later."
        )

    @all_requests
    def user_soft_deleted(self, url, request):
        return self._create_response(
            status_code=404,
            id="1052",
            name="User Soft Deleted",
            message="The user you are making this request for has been soft deleted."
        )

    @all_requests
    def user_deleted(self, url, request):
        return self._create_response(
            status_code=410,
            id="1053",
            name="User Deleted",
            message="The user you are making this request for has been deleted."
        )

    @all_requests
    def not_within_surveymonkey_error_code_range(self, url, request):
        return self._create_response(
            status_code=9001,
            id="9001",
            name="Out of SurveyMonkey range error",
            message="This is an error code that is not within the normal ranges"
        )

    @all_requests
    def status_2xx(self, url, request):
        return self._create_response(
            status_code=201,
            id="201",
            name="Created",
            message="This will test a 2xx status does not raise an exception"
        )

    @all_requests
    def status_3xx(self, url, request):
        return self._create_response(
            status_code=303,
            id="303",
            name="See Other",
            message="This will test a 3xx status does not raise an exception"
        )

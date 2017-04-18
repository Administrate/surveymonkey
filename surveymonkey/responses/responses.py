# -*- coding: utf-8 -*-
from __future__ import absolute_import

import arrow
from cerberus import Validator

from surveymonkey.manager import BaseManager
from surveymonkey.constants import URL_RESPONSE_DETAIL
from surveymonkey.exceptions import SurveyMonkeyBadResponse
from surveymonkey.responses.schemas import RESPONSE_SCHEMA


class Response(BaseManager):

    @staticmethod
    def deserialize_datetimes(response):
        try:
            response['date_created'] = arrow.get(response["date_created"]).datetime
            response['date_modified'] = arrow.get(response["date_modified"]).datetime
        except KeyError:
            pass
        return response

    def parse_response(self, response):
        self.verify_response_json(response)
        return response.json(object_hook=Response.deserialize_datetimes)

    @staticmethod
    def verify_response_json(response):
        try:
            response_data = response.json(object_hook=Response.deserialize_datetimes)
        except (ValueError, AttributeError):
            raise SurveyMonkeyBadResponse("Unable to process the response. Bad JSON.")

        validator = Validator(RESPONSE_SCHEMA)
        validator.allow_unknown = True

        if validator.validate(response_data):
            return True
        else:
            raise SurveyMonkeyBadResponse(validator.errors)

    def by_id(self, survey_id, response_id):
        url = URL_RESPONSE_DETAIL.format(survey_id=survey_id, response_id=response_id)
        return self.get(url)

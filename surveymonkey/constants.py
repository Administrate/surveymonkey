# -*- coding: utf-8 -*-

BASE_URL = "http://www.surveymonkey.com"

API_VERSION = "v3"
API_URL = "https://api.surveymonkey.net/" + API_VERSION

URL_USER_ME = "/users/me"

URL_SURVEYS_DETAIL = "/surveys/{survey_id}/details"
URL_SURVEYS_LIST = "/surveys"
URL_SURVEY_RESPONSES_BULK = "/surveys/{survey_id}/responses/bulk"

URL_FOLDERS_LIST = '/survey_folders'

URL_COLLECTOR_CREATE = "/surveys/{survey_id}/collectors"
URL_COLLECTOR_SINGLE = "/collectors/{collector_id}"
URL_COLLECTOR_RESPONSES_BULK = "/collectors/{collector_id}/responses/bulk"

URL_MESSAGE_CREATE = "/collectors/{collector_id}/messages"
URL_MESSAGE_RECIPIENT_ADD_BULK = "/collectors/{collector_id}/messages/{message_id}/recipients/bulk"  # noqa:E501
URL_MESSAGE_SEND = "/collectors/{collector_id}/messages/{message_id}/send"

URL_RESPONSE_DETAIL = "/surveys/{survey_id}/responses/{response_id}/details"

URL_WEBHOOKS = "/webhooks"

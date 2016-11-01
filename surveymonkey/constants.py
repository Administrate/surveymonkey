# -*- coding: utf-8 -*-

BASE_URL = "http://www.surveymonkey.com"
API_URL = "https://api.surveymonkey.net/v3"

URL_USER_ME = "%s/users/me" % API_URL
URL_SURVEYS_LIST = "%s/surveys" % API_URL

URL_COLLECTOR_CREATE = "%s/surveys/{survey_id}/collectors" % API_URL
URL_COLLECTOR_SINGLE = "%s/collectors" % API_URL
URL_COLLECTOR_RESPONSES_BULK = "%s/collectors/{collector_id}/responses/bulk" % API_URL

URL_MESSAGE_CREATE = "%s/collectors/{collector_id}/messages" % API_URL

URL_WEBHOOKS = "%s/webhooks" % API_URL

URL_SURVEY_RESPONSES_BULK = "%s/surveys/{survey_id}/responses/bulk" % API_URL

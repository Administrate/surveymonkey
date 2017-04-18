from furl import furl


def is_valid_surveymonkey_url(field, value, error):
    smurl = furl(value)
    if smurl.host not in ["api.surveymonkey.net", "www.surveymonkey.com", "surveymonkey.com"]:
        error(field, 'must be a valid SurveyMonkey URL')

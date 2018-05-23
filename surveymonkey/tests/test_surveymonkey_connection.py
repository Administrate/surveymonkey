from __future__ import absolute_import

from expects import be_none, equal, expect

from surveymonkey.surveymonkey import SurveyMonkeyConnection


class TestSurveyMonkeyConnection(object):

    @staticmethod
    def _new_connection(access_url):
        return SurveyMonkeyConnection('access_token', access_url)

    def test_init_without_access_url_has_attribute_set_to_null(self):
        connection = self._new_connection(None)

        expect(connection.access_url).to(be_none)

    def test_init_with_versioned_url_and_no_trailing_slash_is_left_as_it_is(self):
        given_url = 'https://api.surveymonkey.ca/v2'
        connection = self._new_connection(given_url)

        expect(connection.access_url).to(equal(given_url))

    def test_init_with_versioned_url_is_stored_without_trailing_slash(self):
        given_url = 'https://api.surveymonkey.ca/v2/'
        connection = self._new_connection(given_url)

        expect(connection.access_url).to(equal(given_url[0:-1]))

    def test_init_with_unversioned_url_and_trailing_slash_is_stored_with_v3_path(self):
        given_url = 'https://api.surveymonkey.ca/'
        connection = self._new_connection(given_url)

        expect(connection.access_url).to(equal(given_url + 'v3'))

    def test_init_with_unversioned_url_and_no_trailing_slash_is_stored_with_v3_path(self):
        given_url = 'https://api.surveymonkey.ca'
        connection = self._new_connection(given_url)

        expect(connection.access_url).to(equal(given_url + '/v3'))

    def test_init_with_url_with_custom_path_is_left_as_it_is(self):
        given_url = 'https://api.surveymonkey.ca/some/random/path'
        connection = self._new_connection(given_url)

        expect(connection.access_url).to(equal(given_url))

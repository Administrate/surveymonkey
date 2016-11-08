#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from expects import expect, equal, have_key, have_length

from surveymonkey.tests.mocks.surveys import SurveyListMock


class TestSurveyMocksCount(object):  # Quis custodiet ipsos custodes?

    def test_survey_count_is_equal_to_total_surveys_when_total_is_less_than_per_page(self):
        mock = SurveyListMock(total=20)
        remaining = mock.calculate_number_remaining(per_page=50, current_page=1)
        expect(remaining).to(equal(20))

    def test_survey_count_is_zero_when_exceed_the_number_of_possible_pages(self):
        mock = SurveyListMock(total=125)
        remaining = mock.calculate_number_remaining(per_page=50, current_page=4)
        expect(remaining).to(equal(0))

    def test_survey_count_is_correctly_reported_when_there_is_more_than_one_page(self):
        mock = SurveyListMock(total=125)
        remaining = mock.calculate_number_remaining(per_page=50, current_page=2)
        expect(remaining).to(equal(75))


class TestSurveyMocksLinks(object):

    def setup_class(self):
        self.mock = SurveyListMock(total=100)

    def test_links_contains_self_when_it_is_the_first_page(self):
        links = self.mock.get_links(per_page=50, current_page=1, pages=2)
        expect(links).to(have_key('self'))

    def test_links_contains_self_when_it_is_the_last_page(self):
        links = self.mock.get_links(per_page=50, current_page=2, pages=2)
        expect(links).to(have_key('self'))

    def test_links_contains_self_when_current_page_exceeds_total_pages(self):
        links = self.mock.get_links(per_page=50, current_page=4, pages=2)
        expect(links).to(have_key('self'))

    def test_links_contains_self_when_current_page_valid_and_not_first_or_last(self):
        links = self.mock.get_links(per_page=10, current_page=3, pages=10)
        expect(links).to(have_key('self'))

    def test_links_does_not_contain_first_when_on_first_page(self):
        links = self.mock.get_links(per_page=50, current_page=1, pages=2)
        expect(links).not_to(have_key('first'))

    def test_links_contains_first_when_on_last_page(self):
        links = self.mock.get_links(per_page=50, current_page=2, pages=2)
        expect(links).to(have_key('first'))

    def test_links_contains_first_when_current_page_exceeds_total_pages(self):
        links = self.mock.get_links(per_page=50, current_page=4, pages=2)
        expect(links).to(have_key('first'))

    def test_links_contains_first_when_current_page_valid_and_not_first(self):
        links = self.mock.get_links(per_page=10, current_page=4, pages=10)
        expect(links).to(have_key('first'))

    def test_links_does_not_contain_last_when_on_last_page(self):
        links = self.mock.get_links(per_page=50, current_page=2, pages=2)
        expect(links).not_to(have_key('last'))

    def test_links_contains_last_when_on_first_page(self):
        links = self.mock.get_links(per_page=50, current_page=1, pages=2)
        expect(links).to(have_key('last'))

    def test_links_contains_last_when_current_page_exceeds_total_pages(self):
        links = self.mock.get_links(per_page=50, current_page=6, pages=2)
        expect(links).to(have_key('last'))

    def test_links_contains_last_when_current_page_valid_and_not_last(self):
        links = self.mock.get_links(per_page=25, current_page=2, pages=4)
        expect(links).to(have_key('last'))

    def test_links_contains_next_when_on_first_and_there_is_more_than_one_page(self):
        links = self.mock.get_links(per_page=50, current_page=1, pages=2)
        expect(links).to(have_key('next'))

    def test_links_contains_next_when_current_page_valid_and_not_last(self):
        links = self.mock.get_links(per_page=25, current_page=2, pages=4)
        expect(links).to(have_key('next'))

    def test_links_does_not_contain_next_on_last_page(self):
        links = self.mock.get_links(per_page=25, current_page=4, pages=4)
        expect(links).not_to(have_key('next'))

    def test_links_does_not_contain_next_when_current_page_exceeds_total_pages(self):
        links = self.mock.get_links(per_page=50, current_page=6, pages=2)
        expect(links).not_to(have_key('next'))

    def test_links_contains_prev_when_on_last_page(self):
        links = self.mock.get_links(per_page=10, current_page=10, pages=10)
        expect(links).to(have_key('prev'))

    def test_links_contains_prev_when_current_page_exceeds_total_pages(self):
        links = self.mock.get_links(per_page=10, current_page=12, pages=10)
        expect(links).to(have_key('prev'))

    def test_links_does_not_contain_prev_when_on_first_page(self):
        links = self.mock.get_links(per_page=50, current_page=1, pages=2)
        expect(links).not_to(have_key('prev'))

    def test_links_contains_prev_when_current_page_valid_and_not_first_page(self):
        links = self.mock.get_links(per_page=20, current_page=3, pages=5)
        expect(links).to(have_key('prev'))


class TestSurveyMocksCreateSurveys(object):

    def setup_class(self):
        self.mock = SurveyListMock(total=290)

    def test_surveys_empty_when_remaining_is_zero(self):
        surveys = self.mock.create_surveys(per_page=50, current_page=7, pages=6)
        expect(surveys).to(have_length(0))

    def test_surveys_is_equal_to_per_page_when_remaining_is_greater_than_per_page(self):
        surveys = self.mock.create_surveys(per_page=50, current_page=2, pages=6)
        expect(surveys).to(have_length(50))

    def test_surveys_is_equal_to_remaining_when_remaining_is_less_than_per_page(self):
        surveys = self.mock.create_surveys(per_page=50, current_page=6, pages=6)
        expect(surveys).to(have_length(40))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest
from httmock import HTTMock
from expects import expect, end_with, have_keys, have_length, contain

from surveymonkey.folders import Folders
from surveymonkey.exceptions import SurveyMonkeyBadResponse
from surveymonkey.tests.mocks.folders import FolderListMock

from surveymonkey.tests.utils import create_fake_connection


folder_mocks = FolderListMock(total=125)
malformed_response_mocks = [
        folder_mocks.folders_no_data,
        folder_mocks.folders_no_links
]


class TestFolderList(object):

    def setup_class(self):
        self.ACCESS_TOKEN, self.connection = create_fake_connection()

    def setup_method(self, method):
        self.mocks = folder_mocks
        self.folders = Folders(self.connection)

    def test_get_first_page_of_folders(self):
        with HTTMock(self.mocks.folders):
            folders_list = self.folders.folders(page=1)

        expect(folders_list).to(have_length(50))
        expect(folders_list[0]).to(have_keys('href', 'num_surveys', 'id', 'title'))

    def test_get_big_list_of_all_folders(self):
        with HTTMock(self.mocks.folders):
            folder_big_list = self.folders.folders()

        expect(folder_big_list).to(have_length(125))

        for folder in folder_big_list:
            expect(folder).to(have_keys('href', 'num_surveys', 'id', 'title'))
            expect(folder["href"]).to(end_with(folder['id']))

    def test_get_folder_list_by_valid_page_number(self):
        with HTTMock(self.mocks.folders):
            folder_list = self.folders.folders(per_page=10, page=3)

        expect(folder_list).to(have_length(10))
        expect(folder_list[0]).to(have_keys('href', 'num_surveys', 'id', 'title'))

    @pytest.mark.parametrize("mock", malformed_response_mocks)
    def test_surveymonkey_malformed_responses(self, mock):
        with HTTMock(mock):
            with pytest.raises(SurveyMonkeyBadResponse) as e:
                self.folders.folders()

            expect(str(e.value)).to(contain("Missing keys"))

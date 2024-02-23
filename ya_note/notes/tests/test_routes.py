from http import HTTPStatus

from notes.tests.common_test import (
    URL_ADD, URL_DONE, URL_HOME, URL_LIST, URL_LOGIN,
    URL_LOGOUT, URL_SIGNUP, SetUpTestData
)


class TestRoutes(SetUpTestData):

    def test_pages_availability(self):
        for client in (self.client, self.author_client):
            for url in (URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP):
                with self.subTest():
                    response = client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_authorised_user(self):
        for url in (URL_ADD, URL_LIST, URL_DONE):
            with self.subTest():
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_edit_note_and_delete(self):
        client_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.stranger_client, HTTPStatus.NOT_FOUND),
        )
        urls = (self.url_edit, self.url_delete, self.url_detail)
        for client, status in client_statuses:
            for url in urls:
                with self.subTest():
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (self.url_edit, self.url_delete, self.url_detail,
                URL_ADD, URL_DONE, URL_LIST)
        for url in urls:
            with self.subTest():
                redirect_url = f'{URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

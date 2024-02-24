from http import HTTPStatus

from notes.tests.common_test import (
    URL_ADD, URL_DONE, URL_HOME, URL_LIST, URL_LOGIN,
    URL_LOGOUT, URL_SIGNUP, SetUpTestData
)


class TestRoutes(SetUpTestData):

    def test_urls_availability(self):
        client_statuses = (
            (self.author_client, HTTPStatus.OK, HTTPStatus.OK, HTTPStatus.OK),
            (self.stranger_client, HTTPStatus.NOT_FOUND, HTTPStatus.OK,
             HTTPStatus.OK),
            (self.client, HTTPStatus.FOUND, HTTPStatus.FOUND, HTTPStatus.OK)
        )
        url_1 = (self.url_edit, self.url_delete, self.url_detail)
        url_2 = (URL_ADD, URL_LIST, URL_DONE)
        url_3 = (URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP)
        for url in (url_1 + url_2 + url_3):
            for client, status_1, status_2, status_3 in client_statuses:
                with self.subTest():
                    response = client.get(url)
                    if url in url_1:
                        self.assertEqual(response.status_code, status_1)
                    elif url in url_2:
                        self.assertEqual(response.status_code, status_2)
                    else:
                        self.assertEqual(response.status_code, status_3)

    def test_redirect_for_anonymous_client(self):
        urls = (self.url_edit, self.url_delete, self.url_detail,
                URL_ADD, URL_DONE, URL_LIST)
        for url in urls:
            with self.subTest():
                redirect_url = f'{URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

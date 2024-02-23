from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize('url', (
    pytest.lazy_fixture('home_url'),
    pytest.lazy_fixture('detail_url'),
    pytest.lazy_fixture('login_url'),
    pytest.lazy_fixture('logout_url'),
    pytest.lazy_fixture('signup_url'),
))
def test_pages_availability_for_anonymous_user(
    client, url, home_url, detail_url, login_url, logout_url, signup_url
):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'diff_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'url', (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture('edit_url'))
)
def test_pages_availability_for_comment_edit_and_delete(
        diff_client, expected_status, url, delete_url, edit_url, comment):
    response = diff_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url', (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture('edit_url'))
)
def test_redirects(client, url, delete_url, edit_url, login_url):
    assertRedirects(client.get(url), f'{login_url}?next={url}')

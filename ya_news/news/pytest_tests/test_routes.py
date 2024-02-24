from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'diff_client, status_edit_delete, status_others',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK, HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND,
         HTTPStatus.OK),
        (pytest.lazy_fixture('client'), HTTPStatus.FOUND, HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'url', (
        pytest.lazy_fixture('delete_url'),
        pytest.lazy_fixture('edit_url'),
        pytest.lazy_fixture('home_url'),
        pytest.lazy_fixture('detail_url'),
        pytest.lazy_fixture('login_url'),
        pytest.lazy_fixture('logout_url'),
        pytest.lazy_fixture('signup_url'),
    )
)
def test_pages_availability_for_comment_edit_and_delete(
        diff_client, status_edit_delete, status_others,
        url, comment, delete_url, edit_url, home_url, detail_url,
        login_url, logout_url, signup_url
):
    response = diff_client.get(url)
    if url in [delete_url, edit_url]:
        assert response.status_code == status_edit_delete
    else:
        assert response.status_code == status_others


@pytest.mark.parametrize(
    'url', (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture('edit_url'))
)
def test_redirects(client, url, delete_url, edit_url, login_url):
    assertRedirects(client.get(url), f'{login_url}?next={url}')

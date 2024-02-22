from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data={'text': COMMENT_TEXT})
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author, author_client, detail_url, news):
    response = author_client.post(detail_url, data={'text': COMMENT_TEXT})
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client, comment, delete_url, url_to_comments):
    assert Comment.objects.count() == 1
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, delete_url):
    assert Comment.objects.count() == 1
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
        author_client, comment, edit_url, url_to_comments):
    response = author_client.post(edit_url, data={'text': NEW_COMMENT_TEXT})
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, edit_url):
    response = not_author_client.post(edit_url,
                                      data={'text': NEW_COMMENT_TEXT})
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT

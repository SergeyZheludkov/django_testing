from http import HTTPStatus
import pytest

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import FORM_DATA, FORM_DATA_NEW


def test_anonymous_user_cant_create_comment(client, detail_url,
                                            login_url):
    initial_comment_count = Comment.objects.count()
    response = client.post(detail_url, data=FORM_DATA)
    assertRedirects(response, f'{login_url}?next={detail_url}')
    assert Comment.objects.count() == initial_comment_count


def test_user_can_create_comment(author, author_client, detail_url, news):
    initial_comment_count = Comment.objects.count()
    pk_list = [comment.pk for comment in Comment.objects.all()]
    response = author_client.post(detail_url, data=FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == initial_comment_count + 1
    comment = Comment.objects.exclude(pk__in=pk_list).get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    initial_comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == initial_comment_count


def test_author_can_delete_comment(
        author_client, comment, delete_url, url_to_comments):
    initial_comment_count = Comment.objects.count()
    initial_pk = comment.id
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == initial_comment_count - 1
    assert Comment.objects.filter(pk=initial_pk).exists() is False


def test_author_can_edit_comment(author_client, comment,
                                 edit_url, url_to_comments):
    initial_comment_count = Comment.objects.count()
    response = author_client.post(edit_url, data=FORM_DATA_NEW)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == initial_comment_count
    comment = Comment.objects.get(pk=comment.id)
    assert comment.text == FORM_DATA_NEW['text']


@pytest.mark.parametrize(
    'url', (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture('edit_url'))
)
def test_user_cant_delete_and_edit_comment_of_another_user(
    url, not_author_client, comment, delete_url, edit_url,
):
    initial_comment_count = Comment.objects.count()
    initial_comment = (comment.text, comment.news, comment.author)
    if url == edit_url:
        response = not_author_client.post(url)
    else:
        response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_comment_count
    comment = Comment.objects.get(pk=comment.id)
    assert (comment.text, comment.news, comment.author) == initial_comment

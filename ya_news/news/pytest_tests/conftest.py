from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def news_id(news):
    return (news.id,)


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(news=news, author=author,
                                  text='Текст комментария')


@pytest.fixture
def comment_id(comment):
    return (comment.id,)


@pytest.fixture
def news_bulk_creation():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_bulk_creation(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def detail_url(news_id):
    return reverse('news:detail', args=news_id)


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'


@pytest.fixture
def edit_url(comment_id):
    return reverse('news:edit', args=comment_id)


@pytest.fixture
def delete_url(comment_id):
    return reverse('news:delete', args=comment_id)

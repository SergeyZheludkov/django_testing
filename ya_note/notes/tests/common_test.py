from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy

from notes.models import Note

User = get_user_model()

NOTE_TITLE = 'title'
NOTE_TEXT = 'text'
NOTE_SLUG = 'Slug'
FIRST_SLUG = 'slug_1'
NEW_NOTE_TITLE = 'Title revised'
NEW_NOTE_TEXT = 'Text revised'
NEW_NOTE_SLUG = 'Slug_revised'
URL_ADD = reverse_lazy('notes:add')
URL_DONE = reverse_lazy('notes:success')
URL_HOME = reverse_lazy('notes:home')
URL_LIST = reverse_lazy('notes:list')
URL_LOGIN = reverse_lazy('users:login')
URL_LOGOUT = reverse_lazy('users:logout')
URL_SIGNUP = reverse_lazy('users:signup')


class SetUpTestData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.stranger = User.objects.create(username='Stranger')
        cls.stranger_client = Client()
        cls.stranger_client.force_login(cls.stranger)
        cls.note = Note.objects.create(title=NOTE_TITLE, text=NOTE_TEXT,
                                       slug=FIRST_SLUG, author=cls.author,)
        cls.form_data = {'title': NOTE_TITLE, 'text': NOTE_TEXT,
                         'slug': NOTE_SLUG}
        cls.form_data_same = {'title': NOTE_TITLE, 'text': NOTE_TEXT,
                              'slug': FIRST_SLUG}
        cls.form_data_new = {'title': NEW_NOTE_TITLE,
                             'text': NEW_NOTE_TEXT, 'slug': NEW_NOTE_SLUG}
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.note.slug,))
        cls.url_detail = reverse('notes:detail', args=(cls.note.slug,))

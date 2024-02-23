from notes.forms import NoteForm
from notes.tests.common_test import URL_ADD, URL_LIST, SetUpTestData


class TestContent(SetUpTestData):

    def test_note_in_list_for_different_users(self):
        users_inclusion = (
            (self.author, True),
            (self.stranger, False),
        )
        for user, inclusion in users_inclusion:
            self.client.force_login(user)
            response = self.client.get(URL_LIST)
            object_list = response.context['object_list']
            self.assertIs(self.note in object_list, inclusion)

    def test_pages_contains_form(self):
        for url in (URL_ADD, self.url_edit):
            with self.subTest():
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

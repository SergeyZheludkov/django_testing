from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.common_test import (
    FIRST_SLUG, NOTE_TEXT, NOTE_TITLE,
    URL_ADD, URL_DONE, URL_LOGIN, SetUpTestData
)


class TestLogic(SetUpTestData):

    def test_anonymous_user_cant_create_note(self):
        initial_notes_count = Note.objects.count()
        response = self.client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, f'{URL_LOGIN}?next={URL_ADD}')
        self.assertEqual(Note.objects.count(), initial_notes_count)

    def test_user_can_create_note(self):
        initial_notes_count = Note.objects.count()
        pk_list = [note.pk for note in Note.objects.all()]
        response = self.author_client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, URL_DONE)
        self.assertEqual(Note.objects.count(), initial_notes_count + 1)
        note = Note.objects.exclude(pk__in=pk_list).get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_prohibition_the_same_slug(self):
        initial_notes_count = Note.objects.count()
        response = self.author_client.post(URL_ADD, data=self.form_data_same)
        self.assertFormError(
            response, form='form', field='slug',
            errors=FIRST_SLUG + WARNING
        )
        self.assertEqual(Note.objects.count(), initial_notes_count)

    def test_blank_slug(self):
        initial_notes_count = Note.objects.count()
        pk_list = []
        for note in Note.objects.all():
            pk_list.append(note.pk)
        self.form_data['slug'] = ''
        response = self.author_client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, URL_DONE)
        self.assertEqual(Note.objects.count(), initial_notes_count + 1)
        new_note = Note.objects.exclude(pk__in=pk_list).get()
        self.assertEqual(new_note.slug, slugify(new_note.title))

    def test_author_can_delete_note(self):
        initial_notes_count = Note.objects.count()
        response = self.author_client.delete(self.url_delete)
        self.assertRedirects(response, URL_DONE)
        self.assertEqual(Note.objects.count(), initial_notes_count - 1)

    def test_author_can_edit_note(self):
        initial_notes_count = Note.objects.count()
        response = self.author_client.post(self.url_edit,
                                           data=self.form_data_new)
        self.assertRedirects(response, URL_DONE)
        note = Note.objects.get(pk=self.note.id)
        self.assertEqual(note.title, self.form_data_new['title'])
        self.assertEqual(note.text, self.form_data_new['text'])
        self.assertEqual(note.slug, self.form_data_new['slug'])
        self.assertEqual(Note.objects.count(), initial_notes_count)

    def test_user_cant_delete_and_edit__note_of_another_user(self):
        for url in (self.url_delete, self.url_edit):
            with self.subTest():
                initial_notes_count = Note.objects.count()
                if url == self.url_delete:
                    response = self.stranger_client.delete(self.url_delete)
                else:
                    response = self.stranger_client.post(
                        self.url_edit, data=self.form_data_new
                    )
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertEqual(Note.objects.count(), initial_notes_count)
                note = Note.objects.get(pk=self.note.id)
                self.assertEqual(note.title, NOTE_TITLE)
                self.assertEqual(note.text, NOTE_TEXT)
                self.assertEqual(note.slug, FIRST_SLUG)

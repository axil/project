from django.test import TestCase
from notes.models import Category, Notes
from notes.forms import NoteForm


class NotesModelTest(TestCase):
    title = 'create_note'
    text = '<p> good </p>'
    category_name = 'TODO'
    def setUp(self):
        Category.objects.create(name=self.category_name)
        Notes.objects.create(title=self.title, text=self.text)
    def test_filter(self):
        print(self.title)
        self.assertEqual(print(Notes.objects.get(title=self.title)),
                         print(self.title))
        self.assertEqual(print(Category.objects.get(name=self.category_name)),
                         print(self.category_name))
        form = NoteForm({
            'title': self.title,
            'text': self.text,
            'publish': True,
        })
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.title, self.title)
        self.assertEqual(comment.text, self.text)
        self.assertEqual(print(Notes.objects.get(publish=True)),
                         print(self.title))

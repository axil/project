from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class Notes(models.Model):
    class Meta:
        db_table = 'Notes'
        verbose_name_plural = "Заметки"

    def __str__(self):
        return self.title

    title = models.CharField(max_length=150)
    text = RichTextField(null=True, blank=True)
    date = models.DateTimeField()
    author = models.ForeignKey(User)
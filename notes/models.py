from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
# Create your models here.


class Notes(models.Model):
    class Meta:
        db_table = 'Notes'
        verbose_name_plural = "Заметки"

    def __str__(self):
        return self.title
    uuID = u'' + str(uuid.uuid1().hex)
    id = models.UUIDField(primary_key=True, default=uuID, editable=False)
    # slug = models.SlugField(unique=True)
    # slug = models.SlugField(unique=True)
    title = models.CharField(max_length=150)
    text = RichTextField(null=True, blank=True)
    date = models.DateTimeField()
    author = models.ForeignKey(User)
    favorites = models.BooleanField(default=False)
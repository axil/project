from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils.datetime_safe import datetime
import mptt
from mptt.models import MPTTModel, TreeForeignKey
import uuid


class Category(MPTTModel):
    class Meta():
        db_table = 'Category'
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        ordering = ('tree_id', 'level')

    name = models.CharField(max_length=150)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children',
                            verbose_name='parent class')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_py = ['name']


mptt.register(Category, order_insertion_by=['name'])


class Notes(models.Model):
    class Meta:
        db_table = 'Notes'
        verbose_name_plural = "Заметки"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    text = RichTextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # todo должно быть два поля с датой: added и modified
    # первое с auto_new_add второе с auto_now
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    favorites = models.BooleanField(default=False)
    category = models.ForeignKey(Category, blank=True,
                                 null=True, related_name='cat')
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title

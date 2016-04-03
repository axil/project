from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
import mptt
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


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

    def __str__(self):
        return self.title
    # uuID = u'' + str(uuid.uuid1().hex)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4().hex, editable=False)
    # slug = models.SlugField(unique=True)
    # slug = models.SlugField(unique=True)
    title = models.CharField(max_length=150)
    text = RichTextField(null=True, blank=True)
    date = models.DateTimeField()
    author = models.ForeignKey(User)
    favorites = models.BooleanField(default=False)
    category = TreeForeignKey(Category, blank=True, null=True)

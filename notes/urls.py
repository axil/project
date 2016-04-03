from django.conf.urls import url
import notes.views

urlpatterns = [
    url(r'^$', notes.views.notes),
    # url(r'^/sort/(?P<second>\w+)$', notes.views.notes),
    # url(r'^$', notes.views.note)
    # url(r'^(?P<id>[\w*])/$', , name='detail')
    # url(r'^category/get/(?P<category_id>\d+)/$', blog.views.articl_cat, name='category'),
    url(r'^create/$', notes.views.note_create),
    url(r'^category/get/(?P<category_id>\d+)/$', notes.views.category, name='category'),
    url(r'^note/(?P<id>.+)(/del/)$', notes.views.note_del, name='del'),
    url(r'^note/(?P<id>.+)(/edit/)$', notes.views.note_edit, name='edit'),
    url(r'^note/(?P<id>.+)$', notes.views.note, name='notes'),

]

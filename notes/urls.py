from django.conf.urls import url
import notes.views

urlpatterns = [
    url(r'^$', notes.views.notes),
    url(r'^mynotes/', notes.views.mynotes),
    url(r'^create/$', notes.views.note_create),
    url(r'^category/get/(?P<category_id>\d+)/$', notes.views.category, name='category'),
    url(r'^sort/category/$', notes.views.categorysort),
    url(r'^sort/category/ajax/$', notes.views.sort_ajax),
    url(r'^sort/favorites/$', notes.views.favorites),
    url(r'^filter/week/$', notes.views.filter_week),
    url(r'^filter/favorites/$', notes.views.filter_favorites),
    url(r'^note/(?P<id>.+)(/del/)$', notes.views.note_del, name='del'),
    url(r'^note/(?P<id>.+)(/edit/)$', notes.views.note_edit, name='edit'),
    url(r'^note/(?P<id>.+)(/addfavorites/)$', notes.views.addfavorites, name='addfavorites'),
    url(r'^note/(?P<id>.+)(/removefavorites/)$', notes.views.removefavorites, name='removefavorites'),
    url(r'^note/(?P<id>.+)$', notes.views.note, name='note'),

]

from django.conf.urls import url
import notes.views

urlpatterns = [
    url(r'^$', notes.views.notes),
    # url(r'^$', notes.views.note)
    # url(r'^(?P<id>[\w*])/$', , name='detail')
    # url(r'^category/get/(?P<category_id>\d+)/$', blog.views.articl_cat, name='category'),
    url(r'^category/get/(?P<category_id>\d+)/$', notes.views.category, name='category'),
    url(r'^(?P<id>.+)/$', notes.views.note, name='detail'),

]

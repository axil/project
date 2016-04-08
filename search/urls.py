from django.conf.urls import url, include, patterns
import search.views


urlpatterns = [
    url(r'^search-form/$', search.views.search_form, name='filter_title'),
    url(r'^fillter_title/$', search.views.fillter_title),                               # todo лишняя l
    url(r'^$', search.views.search),
]

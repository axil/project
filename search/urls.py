from django.conf.urls import url, include, patterns
import search.views


urlpatterns = [
    url(r'^search-form/$', search.views.search_form, name='form_filter_title'),
    url(r'^filter_title/$', search.views.filter_title, name='filter_title'),
    url(r'^$', search.views.search, name='search'),
]

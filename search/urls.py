from django.conf.urls import url, include, patterns
import search.views


urlpatterns = [
    # url(r'^search-form/$', search.search_form),
    url(r'^$', search.views.search),
]

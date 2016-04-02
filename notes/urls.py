from django.conf.urls import url
import notes.views

urlpatterns = [
    url(r'^$', notes.views.hello),
]

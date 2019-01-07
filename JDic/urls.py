from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.search, name='index'),
    url(r'^(?P<word_id>[a-z][A-Z]+)/$', views.word, name='word'),
    url(r'^search$', views.search),
    url(r'^searchjisho$', views.searchjisho),
    url(r'^addkanji$', views.addkanji),
    url(r'^delkanji$', views.delkanji),
    url(r'^next$', views.next_page)
]   

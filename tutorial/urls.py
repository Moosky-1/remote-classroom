from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listing, name="tutorial-listing"),
    url(r'^list/(?P<id>\w{0,50})/$', views.lists, name="tutorial-lists"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^update/(?P<tutorialId>\w{0,50})/$', views.update, name="update"),
    url(r'^read/(?P<tutorialId>\w{0,50})/$', views.read, name="read"),
]

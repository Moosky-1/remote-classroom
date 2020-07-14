from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listing, name="listing"),
    url(r'^result_view$', views.result_view, name="result_view"),
    url(r'^add$', views.add, name="add"),
    url(r'^quiz/(?P<id>\w{0,50})/$', views.quiz, name="quiz"),
    url(r'^result_answer/(?P<id>\w{0,50})/$', views.result_answer, name="result_answer"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^update/(?P<questionId>\w{0,50})/$', views.update, name="update"),
]

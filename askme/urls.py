from django.conf.urls import url

from askme import views

urlpatterns = [
    url(r'^datetime/$', views.current_datetime),
    url(r'^helloworld/$', views.hello_world),
    url(r'^test/$', views.test),



    url(r'^best/$', views.best, name='best'),
    url(r'^best/(?P<page>[0-9]+)/$', views.best, name='best_page'),

    url(r'^tag/(?P<tag_name>\w+)/$', views.tag, name='tag'),
    url(r'^tag/(?P<tag_name>\w+)/(?P<page>[0-9]+)/$', views.tag, name='tag_page'),

    url(r'^question/(?P<question_id>[0-9]+)/$', views.question, name='question'),

    url(r'^questions/$', views.questions, name='questions'),
    url(r'^questions/(?P<page>[0-9]+)/$', views.questions,  name='questions_page'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),


    url(r'^ask/$', views.ask, name='ask'),

    url(r'^$', views.questions, name='home'),
]

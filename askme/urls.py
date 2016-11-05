from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^datetime/$', views.current_datetime),
    url(r'^helloworld/$', views.hello_world),
    url(r'^test/$', views.test),

    url(r'^hot/$', views.hot, name='hot'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.tag),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^questions/(?P<questions_page>[0-9]+)/$', views.questions),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^ask/$', views.ask, name='ask'),
    
    url(r'^$', views.questions, name='home'),
]

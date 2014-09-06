from django.conf.urls import patterns, url

from theayudar import views
from theayudar import userviews

urlpatterns = patterns('',
    url(r'^theayudar/coo/$', views.test_count_session, name='theayudarcoo'),
    url(r'^index/$', views.index, name='theayudarindex'),
    url(r'^login/$', userviews.user_login),
    url(r'^logout/$', userviews.user_logout),
    url(r'^myprofile/$', userviews.user_info),
    url(r'^participatingevents/$', userviews.participatingEvents),
    url(r'^upcomingevents/$', userviews.upcomingevents),
    url(r'^events/(?P<event_id>\d+)/$', views.eventdetail, name='detail'),
    url(r'^activate/$', userviews.activate_account),
    url(r'^registertevent/$', userviews.registerEvent),
    url(r'^$', views.indexredirect, name="theayudarindex"),
)

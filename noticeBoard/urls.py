from django.conf.urls import url

from noticeBoard.views import NoticeListView, NoticeCreateView, NoticeUpdateView, NoticeDeleteView

urlpatterns = [
    url(r'^$', NoticeListView.as_view(), name='notices'),
    url(r'^add/$', NoticeCreateView.as_view(), name='add_notice'),
    url(r'^edit/(?P<pk>[0-9]+)/$', NoticeUpdateView.as_view(), name='edit_notice'),
    url(r'^delete/(?P<pk>[0-9]+)/$', NoticeDeleteView.as_view(), name='delete_notice'),
]
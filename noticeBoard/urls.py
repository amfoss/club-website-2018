from django.conf.urls import url

from noticeBoard.views import NoticeListView, NoticeCreateView

urlpatterns = [
    url(r'^$', NoticeListView.as_view(), name='notices'),
    url(r'^add/$', NoticeCreateView.as_view(), name='add_notice'),
]
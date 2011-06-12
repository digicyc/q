from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'^$', 'view_user_list', name="view_user_list"),
    url(r'(?P<username>[\w\d\-]+)/edit/$', 'edit_profile', name="edit_profile"),
    url(r'(?P<username>[\w\d\-]+)/$', 'view_user', name="view_user"),
)

#handling comments
from ebooks.listeners import activity_stream_comment
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted

comment_was_posted.connect(activity_stream_comment)
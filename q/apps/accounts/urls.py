from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('accounts.views',
    url(r'^$', 'view_user_list', name="view_user_list"),

    url(r'admin_required/$', TemplateView.as_view(template_name="accounts/admin_required.html"), name='admin_required'),


    url(r'(?P<username>[\w\d\-]+)/edit/$', 'edit_profile', name="edit_profile"),
    url(r'(?P<username>[\w\d\-]+)/$', 'view_user', name="view_user"),
)

#handling comments
from ebooks.listeners import activity_stream_comment
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted

comment_was_posted.connect(activity_stream_comment)
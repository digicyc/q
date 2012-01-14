from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.generic.simple import redirect_to

from django.contrib.auth.views import password_change_done

urlpatterns = patterns('accounts.views',
    url(r'^$', 'edit_profile', name="edit_profile"), 
    url(r'^password/$', 'edit_password', name="edit_password"), 
    url(r'^password/complete/$',password_change_done, name="password_change_done"), 
    url(r'^invitations/$', 'manage_invitations', name="manage_invitations"),
    url(r'^list/$', 'view_user_list', name="list"),
    url(r'login/$', 'login', name='login'),

    url(r'(?P<username>[\w\d\-\.]+)/$', 'view_user', name="view_user"),
)



#from django.conf.urls.defaults import *
#from django.views.generic import TemplateView

#urlpatterns = patterns('accounts.views',
#    url(r'^$', 'view_user_list', name="view_user_list"),
#
#    url(r'admin_required/$', TemplateView.as_view(template_name="accounts/admin_required.html"), name='admin_required'),
#

#    url(r'(?P<username>[\w\d\-]+)/edit/$', 'edit_profile', name="edit_profile"),
#    url(r'(?P<username>[\w\d\-]+)/$', 'view_user', name="view_user"),
#)

#handling comments
from ebooks.listeners import activity_stream_comment, clear_all_activity_steam_cache
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted

comment_was_posted.connect(activity_stream_comment)
comment_was_posted.connect(clear_all_activity_steam_cache)
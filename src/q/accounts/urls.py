from django.conf.urls.defaults import *
from q.accounts.views import view_user, view_user_list, edit_profile

urlpatterns = patterns('',
    url(r'^$', view_user_list, name="view_user_list"),
    url(r'(?P<username>[\w\d\-]+)/edit/$', edit_profile, name="edit_profile"),
    url(r'(?P<username>[\w\d\-]+)/$', view_user, name="view_user"),
)

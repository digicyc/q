from actstream import actions
from actstream import action

from django.core.cache import cache


def activity_stream_comment(sender, comment, request, *args, **kwargs):
    action.send(request.user, verb='commented on', action_object=comment, target=comment.content_object)

def delete_cache(sender, *args, **kwargs):
    key = kwargs.get(key, None)
    if not None:
        cache.delete(key)
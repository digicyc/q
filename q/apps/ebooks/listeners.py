from actstream import actions
from actstream import action

from django.core.cache import cache


def activity_stream_comment(sender, comment, request, *args, **kwargs):
    action.send(request.user, verb='commented on', action_object=comment, target=comment.content_object)

def clear_all_activity_steam_cache(sender, *args, **kwargs):
    cache.delete("all_activity_stream")

def clear_index_actstream_cache(sender, *args, **kwargs):
    cache.delete("index_activity_stream")
from actstream import actions
from actstream import action

def activity_stream_comment(sender, comment, request, *args, **kwargs):
    action.send(request.user, verb='commented on', action_object=comment, target=comment.content_object)
    
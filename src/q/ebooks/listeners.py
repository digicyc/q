from activity_stream.models import create_activity_item

def activity_stream_comment(sender, comment, request, *args, **kwargs):
    create_activity_item('comment', request.user, comment)
    
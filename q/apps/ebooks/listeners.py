from django.core.cache import cache

from activity_stream.models import create_activity_item

from q.common import invalidate_template_cache

def activity_stream_comment(sender, comment, request, *args, **kwargs):
    invalidate_template_cache('latest_activity_stream')
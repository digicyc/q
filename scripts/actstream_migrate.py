from activity_stream.models import ActivityStreamItem
from actstream import actions
from actstream.signals import action

if __name__ == "__main__":
    old_stream = ActivityStreamItem.objects.all()

    for item in old_stream:
        if item.type.name == "invited":
            registrant = item.first_subject().content_object.registrant
            action.send(item.actor, verb="invited", target=registrant, timestamp=item.created_at)
        if item.type.name == "comment":
            comment = item.first_subject().content_object
            action.send(item.actor, verb="commented on", action_object=comment, target=comment.content_object, timestamp=item.created_at)
        if item.type.name == "upload":
            format = item.first_subject().content_object
            if format is not None:
                action.send(item.actor, verb="uploaded", action_object=format, target=format.ebook, timestamp=item.created_at)
        if item.type.name == "kindle":
            book = item.first_subject().content_object
            action.send(item.actor, verb="sent", target=book, timestamp=item.created_at)
        if item.type.name == "download":
            download = item.first_subject().content_object
            if download is not None:
                action.send(item.actor, verb="downloaded", action_object=download, target=download.book, timestamp=item.created_at)

from q.ebooks.models import Format
def book_count_insert(request):
   count = Format.objects.all().values('ebook').distinct().count()
   return {'book_count': count}


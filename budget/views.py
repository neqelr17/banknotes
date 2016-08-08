from django.views import generic
from budget.models import Publisher

from .models import Publisher

class PublisherList(generic.ListView):
    model = Publisher

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

    def get_queryset(self):
        """get stuff"""
        return Publisher.objects


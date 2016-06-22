from django.views.generic import ListView
from budget.models import Publisher

class PublisherList(ListView):
    model = Publisher

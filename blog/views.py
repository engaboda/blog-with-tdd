from django.views.generic import DeleteView
from .models import Entry

# Create your views here.

class EntryDetail(DeleteView):
    model = Entry
    template_name = 'blog/entry_detail.html'
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404

from .models import Entry

from .forms import CommentForm

# Create your views here.

class EntryDetail(CreateView):
    model = Entry
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entry'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry'] = self.get_object()
        return context
    def get_success_url(self):
        return self.get_object().get_absolute_url()
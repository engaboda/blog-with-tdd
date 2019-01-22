from django.views.generic import ListView

from blog.models import Entry

class HomeView(ListView):
    template_name = 'index.html'
    queryset = Entry.objects.all().order_by('-created_at')
    


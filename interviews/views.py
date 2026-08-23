from django.views.generic import DetailView, ListView

from .models import Interview


class InterviewListView(ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interviews/list.html'


class InterviewDetailView(DetailView):
    model = Interview
    context_object_name = 'interview'
    template_name = 'interviews/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_interviews'] = Interview.objects.exclude(pk=self.object.pk)[:3]
        context['project'] = self.object.related_projects.first()
        return context

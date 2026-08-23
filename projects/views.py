from django.views.generic import DetailView, ListView

from .models import Project, Workshop


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['workshops'] = project.workshops.all()
        context['interviews'] = project.related_interviews.all()
        context['social_highlights'] = project.social_highlights.all()
        return context


class WorkshopDetailView(DetailView):
    model = Workshop
    context_object_name = 'workshop'
    template_name = 'projects/workshop_detail.html'

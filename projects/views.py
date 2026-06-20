from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView

from projects.forms import ProjectForm
from projects.models import Project
from team_finder.utils import paginate


def project_list(request):
    projects = Project.objects.select_related('owner').prefetch_related('participants')
    page_obj = paginate(request, projects)
    return render(request, 'projects/project_list.html', {
        'page_obj': page_obj,
        'query_prefix': '',
    })


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        id=project_id,
    )
    return render(request, 'projects/project-details.html', {'project': project})


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'project_id': self.object.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_edit'] = False
        return ctx


class EditProjectView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    pk_url_kwarg = 'project_id'

    def get_object(self):
        project = super().get_object()
        if project.owner != self.request.user:
            raise PermissionDenied
        return project

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'project_id': self.object.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_edit'] = True
        return ctx


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    is_fav = user.favorites.filter(pk=project.pk).exists()
    if is_fav:
        user.favorites.remove(project)
    else:
        user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorite': not is_fav})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user == project.owner:
        return JsonResponse(
            {'status': 'error', 'message': 'Владелец не может быть участником'},
            status=HTTPStatus.BAD_REQUEST,
        )
    is_participant = project.participants.filter(pk=user.pk).exists()
    if is_participant:
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({'status': 'ok', 'participant': not is_participant})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.FORBIDDEN)
    project.status = Project.Status.CLOSED
    project.save()
    return JsonResponse({'status': 'ok'})


@login_required
def favorite_projects(request):
    projects = (
        request.user.favorites.all()
        .select_related('owner')
        .prefetch_related('participants')
    )
    return render(request, 'projects/favorite_projects.html', {'projects': projects})

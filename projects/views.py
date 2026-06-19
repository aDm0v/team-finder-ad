import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from projects.forms import ProjectForm
from projects.models import Project


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.select_related('owner').prefetch_related('participants')
        paginator = Paginator(projects, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'projects/project_list.html', {
            'page_obj': page_obj,
            'query_prefix': '',
        })


class ProjectDetailView(View):
    def get(self, request, project_id):
        project = get_object_or_404(
            Project.objects.select_related('owner').prefetch_related('participants'),
            id=project_id,
        )
        return render(request, 'projects/project-details.html', {'project': project})


class CreateProjectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'projects/create-project.html', {
            'form': ProjectForm(),
            'is_edit': False,
        })

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projects:detail', project_id=project.id)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


class EditProjectView(LoginRequiredMixin, View):
    def get_project(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            return None, redirect('projects:detail', project_id=project_id)
        return project, None

    def get(self, request, project_id):
        project, redir = self.get_project(request, project_id)
        if redir:
            return redir
        return render(request, 'projects/create-project.html', {
            'form': ProjectForm(instance=project),
            'is_edit': True,
        })

    def post(self, request, project_id):
        project, redir = self.get_project(request, project_id)
        if redir:
            return redir
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', project_id=project.id)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        user = request.user
        if project in user.favorites.all():
            user.favorites.remove(project)
            is_fav = False
        else:
            user.favorites.add(project)
            is_fav = True
        return JsonResponse({'status': 'ok', 'favorite': is_fav})


class ToggleParticipateView(LoginRequiredMixin, View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        user = request.user
        if user == project.owner:
            return JsonResponse(
                {'status': 'error', 'message': 'Владелец не может быть участником'},
                status=400,
            )
        if user in project.participants.all():
            project.participants.remove(user)
            participating = False
        else:
            project.participants.add(user)
            participating = True
        return JsonResponse({'status': 'ok', 'participant': participating})


class CompleteProjectView(LoginRequiredMixin, View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            return JsonResponse({'status': 'error'}, status=403)
        project.status = 'closed'
        project.save()
        return JsonResponse({'status': 'ok'})


class FavoriteProjectsView(LoginRequiredMixin, View):
    def get(self, request):
        projects = (
            request.user.favorites.all()
            .select_related('owner')
            .prefetch_related('participants')
        )
        return render(request, 'projects/favorite_projects.html', {'projects': projects})

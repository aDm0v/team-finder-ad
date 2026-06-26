from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from team_finder.utils import paginate
from users.forms import EditProfileForm, LoginForm, RegisterForm
from users.models import User

FILTER_OWNERS_OF_FAVORITE_PROJECTS = 'owners-of-favorite-projects'
FILTER_OWNERS_OF_PARTICIPATING_PROJECTS = 'owners-of-participating-projects'
FILTER_INTERESTED_IN_MY_PROJECTS = 'interested-in-my-projects'
FILTER_PARTICIPANTS_OF_MY_PROJECTS = 'participants-of-my-projects'

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('projects:list')


def user_detail(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user-details.html', {'user': profile_user})

def user_list(request):
    active_filter = request.GET.get('filter', '')
    users = User.objects.all()

    if request.user.is_authenticated and active_filter:
        if active_filter == FILTER_OWNERS_OF_FAVORITE_PROJECTS:
            fav_projects = request.user.favorites.all()
            users = User.objects.filter(
                owned_projects__in=fav_projects
            ).distinct()

        elif active_filter == FILTER_OWNERS_OF_PARTICIPATING_PROJECTS:
            participating = request.user.participating_projects.all()
            users = User.objects.filter(
                owned_projects__in=participating
            ).distinct()

        elif active_filter == FILTER_INTERESTED_IN_MY_PROJECTS:
            my_projects = request.user.owned_projects.all()
            users = User.objects.filter(
                favorites__in=my_projects
            ).distinct()

        elif active_filter == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
            my_projects = request.user.owned_projects.all()
            users = User.objects.filter(
                participating_projects__in=my_projects
            ).distinct()

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('users:detail', args=[self.request.user.id])


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse('users:detail', args=[self.request.user.id])

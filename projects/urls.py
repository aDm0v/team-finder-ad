from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='list'),
    path('favorites/', views.favorite_projects, name='favorites'),
    path('create-project/', views.CreateProjectView.as_view(), name='create'),
    path('<int:project_id>/', views.project_detail, name='detail'),
    path('<int:project_id>/edit/', views.EditProjectView.as_view(), name='edit'),
    path('<int:project_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:project_id>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
    path('<int:project_id>/complete/', views.complete_project, name='complete'),
]

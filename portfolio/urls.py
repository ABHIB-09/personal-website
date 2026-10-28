from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('experience/', views.ExperienceListView.as_view(), name='experience'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('education/', views.EducationListView.as_view(), name='education'),
    path('certifications/', views.CertificationListView.as_view(), name='certifications'),
    path('research/', views.ResearchListView.as_view(), name='research'),
    path('research/<slug:slug>/', views.ResearchDetailView.as_view(), name='research_detail'),
]
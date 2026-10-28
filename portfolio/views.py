from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Project, Experience, Education, Certification, Research, ProjectImage
from core.models import SkillCategory

class ProjectListView(ListView):
    """List of all projects"""
    model = Project
    template_name = 'portfolio/projects.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True).order_by('-is_featured', 'display_order')

class ProjectDetailView(DetailView):
    """Project detail page"""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_projects'] = Project.objects.filter(
            is_published=True
        ).exclude(id=self.object.id)[:3]
        context['images'] = self.object.images.all()
        return context

class ExperienceListView(ListView):
    """Experience list"""
    model = Experience
    template_name = 'portfolio/experience.html'
    context_object_name = 'experiences'
    
    def get_queryset(self):
        return Experience.objects.filter(is_published=True).order_by('-start_date')

class SkillsView(TemplateView):
    """Skills page"""
    template_name = 'portfolio/skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_categories'] = SkillCategory.objects.filter(is_active=True).prefetch_related('skills')
        return context

class EducationListView(ListView):
    """Education list"""
    model = Education
    template_name = 'portfolio/education.html'
    context_object_name = 'educations'
    
    def get_queryset(self):
        return Education.objects.filter(is_published=True).order_by('-start_date')

class CertificationListView(ListView):
    """Certification list"""
    model = Certification
    template_name = 'portfolio/certifications.html'
    context_object_name = 'certifications'
    
    def get_queryset(self):
        return Certification.objects.filter(is_active=True)

class ResearchListView(ListView):
    """Research list"""
    model = Research
    template_name = 'portfolio/research.html'
    context_object_name = 'research_items'
    paginate_by = 9
    
    def get_queryset(self):
        return Research.objects.filter(is_published=True)

class ResearchDetailView(DetailView):
    """Research detail page"""
    model = Research
    template_name = 'portfolio/research_detail.html'
    context_object_name = 'research'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Research.objects.filter(is_published=True)
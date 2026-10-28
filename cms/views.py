from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
import os
from PIL import Image

from core.models import Profile, WebsiteSettings, SocialLink, Metric, SkillCategory, Skill, ContactMessage
from portfolio.models import Project, Experience, Education, Certification, Research, ProjectImage
from blog.models import BlogPost, BlogCategory
from .models import MediaFile
from .forms import (
    ProfileForm, WebsiteSettingsForm, SocialLinkForm, MetricForm,
    ProjectForm, ExperienceForm, EducationForm, CertificationForm,
    ResearchForm, BlogPostForm, BlogCategoryForm, SkillCategoryForm, SkillForm,
    MediaFileForm, ContactMessageForm
)

# Owner check mixin
class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('core:home')

# Authentication Views
class OwnerLoginView(LoginView):
    template_name = 'cms/login.html'
    
    def get_success_url(self):
        return reverse('cms:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Welcome back!')
        return super().form_valid(form)

class OwnerLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')

# Dashboard View
class DashboardView(OwnerRequiredMixin, TemplateView):
    template_name = 'cms/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Stats
        context['project_count'] = Project.objects.count()
        context['project_published_count'] = Project.objects.filter(is_published=True).count()
        context['experience_count'] = Experience.objects.count()
        context['blog_count'] = BlogPost.objects.count()
        context['blog_published_count'] = BlogPost.objects.filter(is_published=True).count()
        context['research_count'] = Research.objects.count()
        context['research_published_count'] = Research.objects.filter(is_published=True).count()
        context['unread_messages'] = ContactMessage.objects.filter(status='unread').count()
        context['total_messages'] = ContactMessage.objects.count()
        context['media_count'] = MediaFile.objects.count()
        
        # Recent activity
        context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        
        return context

# ========== PROFILE ==========
class ProfileUpdateView(OwnerRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'cms/profile_update.html'
    success_url = reverse_lazy('cms:profile_update')
    
    def get_object(self):
        return Profile.objects.first()
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

# ========== SETTINGS ==========
class SettingsUpdateView(OwnerRequiredMixin, UpdateView):
    model = WebsiteSettings
    form_class = WebsiteSettingsForm
    template_name = 'cms/settings.html'
    success_url = reverse_lazy('cms:settings')
    
    def get_object(self):
        return WebsiteSettings.objects.first()
    
    def form_valid(self, form):
        messages.success(self.request, 'Settings updated successfully!')
        return super().form_valid(form)

# ========== SOCIAL LINKS ==========
class SocialLinkListView(OwnerRequiredMixin, ListView):
    model = SocialLink
    template_name = 'cms/social_links.html'
    context_object_name = 'links'

class SocialLinkCreateView(OwnerRequiredMixin, CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = 'cms/social_link_form.html'
    success_url = reverse_lazy('cms:social_link_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Social link added successfully!')
        return super().form_valid(form)

class SocialLinkUpdateView(OwnerRequiredMixin, UpdateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = 'cms/social_link_form.html'
    success_url = reverse_lazy('cms:social_link_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Social link updated successfully!')
        return super().form_valid(form)

class SocialLinkDeleteView(OwnerRequiredMixin, DeleteView):
    model = SocialLink
    success_url = reverse_lazy('cms:social_link_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Social link deleted successfully!')
        return super().delete(request, *args, **kwargs)

class SocialLinkToggleView(OwnerRequiredMixin, View):
    def post(self, request, pk):
        link = get_object_or_404(SocialLink, pk=pk)
        link.is_active = not link.is_active
        link.save()
        return JsonResponse({'status': 'success', 'is_active': link.is_active})

# ========== METRICS ==========
class MetricListView(OwnerRequiredMixin, ListView):
    model = Metric
    template_name = 'cms/metrics.html'
    context_object_name = 'metrics'

class MetricCreateView(OwnerRequiredMixin, CreateView):
    model = Metric
    form_class = MetricForm
    template_name = 'cms/metric_form.html'
    success_url = reverse_lazy('cms:metric_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Metric added successfully!')
        return super().form_valid(form)

class MetricUpdateView(OwnerRequiredMixin, UpdateView):
    model = Metric
    form_class = MetricForm
    template_name = 'cms/metric_form.html'
    success_url = reverse_lazy('cms:metric_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Metric updated successfully!')
        return super().form_valid(form)

class MetricDeleteView(OwnerRequiredMixin, DeleteView):
    model = Metric
    success_url = reverse_lazy('cms:metric_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Metric deleted successfully!')
        return super().delete(request, *args, **kwargs)

class MetricToggleView(OwnerRequiredMixin, View):
    def post(self, request, pk):
        metric = get_object_or_404(Metric, pk=pk)
        metric.is_active = not metric.is_active
        metric.save()
        return JsonResponse({'status': 'success', 'is_active': metric.is_active})

# ========== PROJECTS ==========
class ProjectListView(OwnerRequiredMixin, ListView):
    model = Project
    template_name = 'cms/projects.html'
    context_object_name = 'projects'
    paginate_by = 20
    
    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')

class ProjectCreateView(OwnerRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'cms/project_form.html'
    success_url = reverse_lazy('cms:project_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

class ProjectUpdateView(OwnerRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'cms/project_form.html'
    success_url = reverse_lazy('cms:project_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

class ProjectDeleteView(OwnerRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('cms:project_list')
    
    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        # Delete associated media files
        for image in project.images.all():
            image.delete()
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ProjectTogglePublishView(OwnerRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.is_published = not project.is_published
        project.save()
        return JsonResponse({'status': 'success', 'is_published': project.is_published})

# ========== EXPERIENCE ==========
class ExperienceListView(OwnerRequiredMixin, ListView):
    model = Experience
    template_name = 'cms/experience.html'
    context_object_name = 'experiences'
    
    def get_queryset(self):
        return Experience.objects.all().order_by('-start_date')

class ExperienceCreateView(OwnerRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'cms/experience_form.html'
    success_url = reverse_lazy('cms:experience_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Experience added successfully!')
        return super().form_valid(form)

class ExperienceUpdateView(OwnerRequiredMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'cms/experience_form.html'
    success_url = reverse_lazy('cms:experience_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Experience updated successfully!')
        return super().form_valid(form)

class ExperienceDeleteView(OwnerRequiredMixin, DeleteView):
    model = Experience
    success_url = reverse_lazy('cms:experience_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Experience deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========== EDUCATION ==========
class EducationListView(OwnerRequiredMixin, ListView):
    model = Education
    template_name = 'cms/education.html'
    context_object_name = 'educations'
    
    def get_queryset(self):
        return Education.objects.all().order_by('-start_date')

class EducationCreateView(OwnerRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'cms/education_form.html'
    success_url = reverse_lazy('cms:education_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education added successfully!')
        return super().form_valid(form)

class EducationUpdateView(OwnerRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'cms/education_form.html'
    success_url = reverse_lazy('cms:education_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

class EducationDeleteView(OwnerRequiredMixin, DeleteView):
    model = Education
    success_url = reverse_lazy('cms:education_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Education deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========== CERTIFICATIONS ==========
class CertificationListView(OwnerRequiredMixin, ListView):
    model = Certification
    template_name = 'cms/certifications.html'
    context_object_name = 'certifications'

class CertificationCreateView(OwnerRequiredMixin, CreateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'cms/certification_form.html'
    success_url = reverse_lazy('cms:certification_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification added successfully!')
        return super().form_valid(form)

class CertificationUpdateView(OwnerRequiredMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'cms/certification_form.html'
    success_url = reverse_lazy('cms:certification_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification updated successfully!')
        return super().form_valid(form)

class CertificationDeleteView(OwnerRequiredMixin, DeleteView):
    model = Certification
    success_url = reverse_lazy('cms:certification_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Certification deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========== SKILLS ==========
class SkillCategoryListView(OwnerRequiredMixin, ListView):
    model = SkillCategory
    template_name = 'cms/skill_categories.html'
    context_object_name = 'categories'

class SkillCategoryCreateView(OwnerRequiredMixin, CreateView):
    model = SkillCategory
    form_class = SkillCategoryForm
    template_name = 'cms/skill_category_form.html'
    success_url = reverse_lazy('cms:skill_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill category added successfully!')
        return super().form_valid(form)

class SkillListView(OwnerRequiredMixin, ListView):
    model = Skill
    template_name = 'cms/skills.html'
    context_object_name = 'skills'
    
    def get_queryset(self):
        return Skill.objects.all().select_related('category')

class SkillCreateView(OwnerRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'cms/skill_form.html'
    success_url = reverse_lazy('cms:skill_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill added successfully!')
        return super().form_valid(form)

class SkillUpdateView(OwnerRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'cms/skill_form.html'
    success_url = reverse_lazy('cms:skill_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill updated successfully!')
        return super().form_valid(form)

class SkillDeleteView(OwnerRequiredMixin, DeleteView):
    model = Skill
    success_url = reverse_lazy('cms:skill_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Skill deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========== RESEARCH ==========
class ResearchListView(OwnerRequiredMixin, ListView):
    model = Research
    template_name = 'cms/research.html'
    context_object_name = 'research_items'
    
    def get_queryset(self):
        return Research.objects.all().order_by('-created_at')

class ResearchCreateView(OwnerRequiredMixin, CreateView):
    model = Research
    form_class = ResearchForm
    template_name = 'cms/research_form.html'
    success_url = reverse_lazy('cms:research_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Research added successfully!')
        return super().form_valid(form)

class ResearchUpdateView(OwnerRequiredMixin, UpdateView):
    model = Research
    form_class = ResearchForm
    template_name = 'cms/research_form.html'
    success_url = reverse_lazy('cms:research_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Research updated successfully!')
        return super().form_valid(form)

class ResearchDeleteView(OwnerRequiredMixin, DeleteView):
    model = Research
    success_url = reverse_lazy('cms:research_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Research deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ResearchTogglePublishView(OwnerRequiredMixin, View):
    def post(self, request, pk):
        research = get_object_or_404(Research, pk=pk)
        research.is_published = not research.is_published
        research.save()
        return JsonResponse({'status': 'success', 'is_published': research.is_published})

# ========== BLOG ==========
class BlogListView(OwnerRequiredMixin, ListView):
    model = BlogPost
    template_name = 'cms/blog.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return BlogPost.objects.all().order_by('-created_at')

class BlogCreateView(OwnerRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'cms/blog_form.html'
    success_url = reverse_lazy('cms:blog_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)

class BlogUpdateView(OwnerRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'cms/blog_form.html'
    success_url = reverse_lazy('cms:blog_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)

class BlogDeleteView(OwnerRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('cms:blog_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Blog post deleted successfully!')
        return super().delete(request, *args, **kwargs)

class BlogTogglePublishView(OwnerRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        post.is_published = not post.is_published
        if post.is_published and not post.published_date:
            post.published_date = timezone.now()
        post.save()
        return JsonResponse({'status': 'success', 'is_published': post.is_published})

class BlogCategoryListView(OwnerRequiredMixin, ListView):
    model = BlogCategory
    template_name = 'cms/blog_categories.html'
    context_object_name = 'categories'

class BlogCategoryCreateView(OwnerRequiredMixin, CreateView):
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'cms/blog_category_form.html'
    success_url = reverse_lazy('cms:blog_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog category added successfully!')
        return super().form_valid(form)

# ========== MESSAGES ==========
class MessageListView(OwnerRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'cms/messages.html'
    context_object_name = 'messages'
    paginate_by = 20
    
    def get_queryset(self):
        return ContactMessage.objects.all().order_by('-created_at')

class MessageDetailView(OwnerRequiredMixin, DetailView):
    model = ContactMessage
    template_name = 'cms/message_detail.html'
    context_object_name = 'message'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Mark as read if unread
        message = self.get_object()
        if message.status == 'unread':
            message.status = 'read'
            message.save()
        return response

class MessageUpdateStatusView(OwnerRequiredMixin, View):
    def post(self, request, pk):
        message = get_object_or_404(ContactMessage, pk=pk)
        status = request.POST.get('status')
        if status in ['unread', 'read', 'replied', 'archived']:
            message.status = status
            message.save()
        return JsonResponse({'status': 'success'})

class MessageDeleteView(OwnerRequiredMixin, DeleteView):
    model = ContactMessage
    success_url = reverse_lazy('cms:message_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Message deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ========== MEDIA ==========
class MediaLibraryView(OwnerRequiredMixin, ListView):
    model = MediaFile
    template_name = 'cms/media_library.html'
    context_object_name = 'files'
    paginate_by = 24
    
    def get_queryset(self):
        return MediaFile.objects.all().order_by('-upload_date')

class MediaUploadView(OwnerRequiredMixin, CreateView):
    model = MediaFile
    form_class = MediaFileForm
    template_name = 'cms/media_upload.html'
    success_url = reverse_lazy('cms:media_library')
    
    def form_valid(self, form):
        messages.success(self.request, 'File uploaded successfully!')
        return super().form_valid(form)

class MediaDeleteView(OwnerRequiredMixin, DeleteView):
    model = MediaFile
    success_url = reverse_lazy('cms:media_library')
    
    def delete(self, request, *args, **kwargs):
        media = self.get_object()
        # Delete the actual file
        if media.file:
            if os.path.isfile(media.file.path):
                os.remove(media.file.path)
        messages.success(request, 'File deleted successfully!')
        return super().delete(request, *args, **kwargs)
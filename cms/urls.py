from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Profile
    path('profile/', views.ProfileUpdateView.as_view(), name='profile_update'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<int:pk>/toggle-publish/', views.ProjectTogglePublishView.as_view(), name='project_toggle_publish'),
    
    # Experience
    path('experience/', views.ExperienceListView.as_view(), name='experience_list'),
    path('experience/add/', views.ExperienceCreateView.as_view(), name='experience_add'),
    path('experience/<int:pk>/edit/', views.ExperienceUpdateView.as_view(), name='experience_edit'),
    path('experience/<int:pk>/delete/', views.ExperienceDeleteView.as_view(), name='experience_delete'),
    
    # Skills
    path('skills/', views.SkillListView.as_view(), name='skill_list'),
    path('skills/add/', views.SkillCreateView.as_view(), name='skill_add'),
    path('skills/<int:pk>/edit/', views.SkillUpdateView.as_view(), name='skill_edit'),
    path('skills/<int:pk>/delete/', views.SkillDeleteView.as_view(), name='skill_delete'),
    path('skills/categories/', views.SkillCategoryListView.as_view(), name='skill_category_list'),
    path('skills/categories/add/', views.SkillCategoryCreateView.as_view(), name='skill_category_add'),
    
    # Education
    path('education/', views.EducationListView.as_view(), name='education_list'),
    path('education/add/', views.EducationCreateView.as_view(), name='education_add'),
    path('education/<int:pk>/edit/', views.EducationUpdateView.as_view(), name='education_edit'),
    path('education/<int:pk>/delete/', views.EducationDeleteView.as_view(), name='education_delete'),
    
    # Certifications
    path('certifications/', views.CertificationListView.as_view(), name='certification_list'),
    path('certifications/add/', views.CertificationCreateView.as_view(), name='certification_add'),
    path('certifications/<int:pk>/edit/', views.CertificationUpdateView.as_view(), name='certification_edit'),
    path('certifications/<int:pk>/delete/', views.CertificationDeleteView.as_view(), name='certification_delete'),
    
    # Research
    path('research/', views.ResearchListView.as_view(), name='research_list'),
    path('research/add/', views.ResearchCreateView.as_view(), name='research_add'),
    path('research/<int:pk>/edit/', views.ResearchUpdateView.as_view(), name='research_edit'),
    path('research/<int:pk>/delete/', views.ResearchDeleteView.as_view(), name='research_delete'),
    path('research/<int:pk>/toggle-publish/', views.ResearchTogglePublishView.as_view(), name='research_toggle_publish'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/add/', views.BlogCreateView.as_view(), name='blog_add'),
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/toggle-publish/', views.BlogTogglePublishView.as_view(), name='blog_toggle_publish'),
    path('blog/categories/', views.BlogCategoryListView.as_view(), name='blog_category_list'),
    path('blog/categories/add/', views.BlogCategoryCreateView.as_view(), name='blog_category_add'),
    
    # Messages
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update-status/', views.MessageUpdateStatusView.as_view(), name='message_update_status'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    
    # Media
    path('media/', views.MediaLibraryView.as_view(), name='media_library'),
    path('media/upload/', views.MediaUploadView.as_view(), name='media_upload'),
    path('media/<int:pk>/delete/', views.MediaDeleteView.as_view(), name='media_delete'),
    
    # Settings
    path('settings/', views.SettingsUpdateView.as_view(), name='settings'),
    
    # Social Links
    path('social-links/', views.SocialLinkListView.as_view(), name='social_link_list'),
    path('social-links/add/', views.SocialLinkCreateView.as_view(), name='social_link_add'),
    path('social-links/<int:pk>/edit/', views.SocialLinkUpdateView.as_view(), name='social_link_edit'),
    path('social-links/<int:pk>/delete/', views.SocialLinkDeleteView.as_view(), name='social_link_delete'),
    path('social-links/<int:pk>/toggle/', views.SocialLinkToggleView.as_view(), name='social_link_toggle'),
    
    # Metrics
    path('metrics/', views.MetricListView.as_view(), name='metric_list'),
    path('metrics/add/', views.MetricCreateView.as_view(), name='metric_add'),
    path('metrics/<int:pk>/edit/', views.MetricUpdateView.as_view(), name='metric_edit'),
    path('metrics/<int:pk>/delete/', views.MetricDeleteView.as_view(), name='metric_delete'),
    path('metrics/<int:pk>/toggle/', views.MetricToggleView.as_view(), name='metric_toggle'),
    
    # Authentication
    path('login/', views.OwnerLoginView.as_view(), name='login'),
    path('logout/', views.OwnerLogoutView.as_view(), name='logout'),
]
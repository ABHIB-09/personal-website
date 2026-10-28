from django import forms
from django.forms import inlineformset_factory
from core.models import Profile, WebsiteSettings, SocialLink, Metric, SkillCategory, Skill, ContactMessage
from portfolio.models import Project, ProjectImage, Experience, Education, Certification, Research
from blog.models import BlogPost, BlogCategory
from .models import MediaFile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['professional_title', 'headline', 'bio', 'about', 'profile_image', 
                  'email', 'phone', 'location', 'availability', 'resume', 'years_experience']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
            'about': forms.Textarea(attrs={'rows': 8}),
        }

class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = WebsiteSettings
        fields = ['site_title', 'site_description', 'logo', 'favicon', 
                  'primary_color', 'secondary_color', 'accent_color',
                  'hero_title', 'hero_subtitle', 'hero_visible', 'projects_visible',
                  'research_visible', 'blog_visible', 'experience_visible', 'contact_visible',
                  'seo_title', 'seo_description', 'seo_keywords']

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url', 'display_order', 'is_active']

class MetricForm(forms.ModelForm):
    class Meta:
        model = Metric
        fields = ['label', 'value', 'icon_class', 'display_order', 'is_active']

class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model = SkillCategory
        fields = ['name', 'icon_class', 'display_order', 'is_active']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name', 'proficiency', 'years_experience', 'is_active', 'display_order']
        widgets = {
            'proficiency': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'slug', 'short_description', 'description', 'problem', 'solution',
                  'my_role', 'architecture', 'technologies', 'business_impact', 'metrics',
                  'github_url', 'live_demo_url', 'video_url', 'video_provider', 'video_file',
                  'video_thumbnail', 'video_title', 'video_duration', 'thumbnail',
                  'is_featured', 'is_published', 'display_order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'problem': forms.Textarea(attrs={'rows': 6}),
            'solution': forms.Textarea(attrs={'rows': 6}),
            'my_role': forms.Textarea(attrs={'rows': 6}),
            'architecture': forms.Textarea(attrs={'rows': 6}),
            'business_impact': forms.Textarea(attrs={'rows': 5}),
            'metrics': forms.Textarea(attrs={'rows': 4}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'role', 'location', 'start_date', 'end_date', 'is_current',
                  'description', 'achievements', 'technologies', 'company_url', 'company_logo',
                  'display_order', 'is_published']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'achievements': forms.Textarea(attrs={'rows': 6}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'location', 'start_date', 'end_date',
                  'is_current', 'description', 'gpa', 'logo', 'display_order', 'is_published']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date',
                  'credential_id', 'credential_url', 'logo', 'is_active', 'display_order']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['title', 'slug', 'subtitle', 'description', 'research_question', 'problem',
                  'architecture', 'methodology', 'evaluation', 'results', 'future_work',
                  'paper_url', 'github_url', 'presentation_url', 'thumbnail',
                  'is_published', 'display_order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'research_question': forms.Textarea(attrs={'rows': 4}),
            'problem': forms.Textarea(attrs={'rows': 4}),
            'architecture': forms.Textarea(attrs={'rows': 5}),
            'methodology': forms.Textarea(attrs={'rows': 5}),
            'evaluation': forms.Textarea(attrs={'rows': 4}),
            'results': forms.Textarea(attrs={'rows': 5}),
            'future_work': forms.Textarea(attrs={'rows': 4}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'excerpt', 'content', 'categories', 'hero_image',
                  'tags', 'reading_time', 'is_published', 'seo_title', 'seo_description']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 15}),
            'categories': forms.SelectMultiple(attrs={'size': 5}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g., Python, AI, Machine Learning'}),
        }

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name', 'slug', 'description', 'is_active']

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'project_type', 'message', 'status']

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['name', 'file', 'file_type', 'description', 'alt_text', 'is_public']
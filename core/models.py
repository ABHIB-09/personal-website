from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class WebsiteSettings(models.Model):
    """Website global settings"""
    site_title = models.CharField(max_length=200, default='AI/ML Engineer Portfolio')
    site_description = models.TextField(default='Building Intelligent Systems for the Real World')
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#1a365d')
    secondary_color = models.CharField(max_length=7, default='#2b6cb0')
    accent_color = models.CharField(max_length=7, default='#3182ce')
    hero_title = models.CharField(max_length=200, default='Building Intelligent Systems for the Real World.')
    hero_subtitle = models.TextField(
        default='AI/ML & Generative AI Engineer building production-grade RAG systems, '
                'Agentic AI applications, intelligent automation and machine learning solutions.'
    )
    hero_visible = models.BooleanField(default=True)
    projects_visible = models.BooleanField(default=True)
    research_visible = models.BooleanField(default=True)
    blog_visible = models.BooleanField(default=True)
    experience_visible = models.BooleanField(default=True)
    contact_visible = models.BooleanField(default=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website Settings'

    def __str__(self):
        return self.site_title


class SocialLink(models.Model):
    """Social media and professional links"""
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('email', 'Email'),
        ('twitter', 'Twitter/X'),
        ('youtube', 'YouTube'),
        ('medium', 'Medium'),
        ('scholar', 'Google Scholar'),
        ('researchgate', 'ResearchGate'),
        ('orcid', 'ORCID'),
        ('kaggle', 'Kaggle'),
        ('portfolio', 'Portfolio'),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=500)
    icon_class = models.CharField(max_length=50, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.get_platform_display()}: {self.url}"


class Profile(models.Model):
    """Owner profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    professional_title = models.CharField(max_length=200, default='AI/ML Engineer')
    headline = models.CharField(max_length=200, default='Building Intelligent Systems for the Real World')
    bio = models.TextField(blank=True)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    availability = models.CharField(max_length=100, default='Available for projects')
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    years_experience = models.DecimalField(max_digits=4, decimal_places=1, default=2.5)

    def __str__(self):
        return f"Profile: {self.user.username}"


class Metric(models.Model):
    """Professional metrics/statistics"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=50, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactMessage(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('AI/ML', 'AI / Machine Learning'),
        ('Generative AI', 'Generative AI'),
        ('RAG', 'RAG Systems'),
        ('AI Agents', 'AI Agents'),
        ('Automation', 'Automation'),
        ('Computer Vision', 'Computer Vision'),
        ('Consulting', 'Consulting'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    project_type = models.CharField(max_length=100, choices=PROJECT_TYPE_CHOICES, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-received_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f'{self.name} | {self.email} | {self.received_at:%d %b %Y %H:%M}'


class SkillCategory(models.Model):
    """Skill categories"""
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual skills"""
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=80, help_text='Proficiency percentage (0-100)')
    years_experience = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.category.name} - {self.name}"
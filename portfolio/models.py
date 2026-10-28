from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import os

class Experience(models.Model):
    """Work experience entries"""
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.TextField(blank=True)
    technologies = models.TextField(blank=True, help_text='Comma-separated technologies')
    company_url = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='experience/logos/', blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.role} at {self.company}"
    
    @property
    def duration(self):
        if self.is_current:
            end = timezone.now().date()
        else:
            end = self.end_date
        if end:
            months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
            years = months // 12
            months = months % 12
            if years > 0 and months > 0:
                return f"{years}y {months}m"
            elif years > 0:
                return f"{years}y"
            else:
                return f"{months}m"
        return ""

class Education(models.Model):
    """Education entries"""
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    logo = models.ImageField(upload_to='education/logos/', blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Education'
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Certification(models.Model):
    """Certifications"""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='certifications/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """Project entries"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(max_length=500)
    description = models.TextField()
    problem = models.TextField(help_text='What problem does this project solve?')
    solution = models.TextField(help_text='How does this project solve the problem?')
    my_role = models.TextField(help_text='What was your role in this project?')
    architecture = models.TextField(blank=True, help_text='High-level architecture description')
    technologies = models.TextField(help_text='Comma-separated technologies used')
    business_impact = models.TextField(blank=True)
    metrics = models.TextField(blank=True, help_text='Key performance metrics')
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    video_provider = models.CharField(max_length=20, blank=True, choices=[
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('local', 'Local'),
        ('other', 'Other'),
    ])
    video_file = models.FileField(upload_to='projects/videos/', blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='projects/video-thumbnails/', blank=True, null=True)
    video_title = models.CharField(max_length=200, blank=True)
    video_duration = models.CharField(max_length=20, blank=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'display_order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio:project_detail', args=[self.slug])
    
    @property
    def technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

class ProjectImage(models.Model):
    """Project gallery images"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"Image for {self.project.title}"

class ProjectTechnology(models.Model):
    """Project technologies (for filtering/search)"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_technologies')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.project.title}"

class Research(models.Model):
    """Research entries"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    research_question = models.TextField(help_text='What research question does this address?')
    problem = models.TextField(help_text='What problem does this research address?')
    architecture = models.TextField(blank=True, help_text='Research architecture/methodology')
    methodology = models.TextField(blank=True)
    evaluation = models.TextField(blank=True)
    results = models.TextField(help_text='What were the findings?')
    future_work = models.TextField(blank=True)
    paper_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    presentation_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='research/thumbnails/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Research'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio:research_detail', args=[self.slug])

class ResearchImage(models.Model):
    """Research images/diagrams"""
    research = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='research/images/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"Image for {self.research.title}"
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class BlogCategory(models.Model):
    """Blog categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Blog Categories'
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """Blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    categories = models.ManyToManyField(BlogCategory, related_name='posts')
    hero_image = models.ImageField(upload_to='blog/hero/', blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    reading_time = models.IntegerField(default=5, help_text='Estimated reading time in minutes')
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

class BlogImage(models.Model):
    """Blog images"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"Image for {self.post.title}"
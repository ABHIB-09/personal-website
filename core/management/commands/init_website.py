from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import WebsiteSettings, Profile, SocialLink, Metric, SkillCategory, Skill
from portfolio.models import Experience, Project, Research
from blog.models import BlogCategory
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Initialize the website with default data'
    
    def handle(self, *args, **options):
        self.stdout.write('Initializing website...')
        
        # Create Website Settings
        settings, created = WebsiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_title': 'AI/ML Engineer Portfolio',
                'site_description': 'Building Intelligent Systems for the Real World',
                'hero_title': 'Building Intelligent Systems for the Real World.',
                'hero_subtitle': 'AI/ML & Generative AI Engineer building production-grade RAG systems, Agentic AI applications, intelligent automation and machine learning solutions.',
                'primary_color': '#1a365d',
                'secondary_color': '#2b6cb0',
                'accent_color': '#3182ce',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Website settings created'))
        
        # Create default admin user if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Default admin user created (username: admin, password: admin123)'))
        
        # Create Profile
        if not Profile.objects.exists():
            profile = Profile.objects.create(
                user=User.objects.first(),
                professional_title='AI/ML & Generative AI Engineer',
                headline='Building Intelligent Systems for the Real World',
                years_experience=2.5,
                availability='Available for projects',
            )
            self.stdout.write(self.style.SUCCESS('Profile created'))
        
        # Create Metrics - Fixed to include icon_class
        metrics_data = [
            ('Years Production Experience', '2.5+', '📊', 0),
            ('AI Inference Latency Reduction', '25%', '⚡', 1),
            ('Operational Efficiency Improvement', '40%', '📈', 2),
            ('Reduction in Manual Data Errors', '60%', '🎯', 3),
            ('Records Processed', '10K+', '💾', 4),
        ]
        for label, value, icon, order in metrics_data:
            Metric.objects.get_or_create(
                label=label,
                defaults={
                    'value': value, 
                    'icon_class': icon, 
                    'display_order': order, 
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS('Metrics created'))
        
        # Create Social Links
        social_links = [
            ('linkedin', 'https://linkedin.com/in/your-profile', 0),
            ('github', 'https://github.com/your-profile', 1),
            ('email', 'mailto:your-email@example.com', 2),
        ]
        for platform, url, order in social_links:
            SocialLink.objects.get_or_create(
                platform=platform,
                defaults={'url': url, 'display_order': order, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS('Social links created'))
        
        # Create Skill Categories and Skills
        categories = [
            ('AI / ML', ['Python', 'PyTorch', 'TensorFlow', 'Scikit-learn', 'Pandas', 'NumPy']),
            ('Generative AI', ['LLMs', 'RAG', 'LangChain', 'LangGraph', 'Hugging Face', 'Prompt Engineering', 'Agents']),
            ('Backend', ['Django', 'FastAPI', 'REST APIs']),
            ('Cloud', ['AWS', 'Bedrock', 'SageMaker', 'Lambda', 'S3']),
            ('Databases', ['PostgreSQL', 'MySQL', 'SQL Server', 'SQLite', 'Qdrant']),
            ('DevOps', ['Docker', 'Nginx', 'Gunicorn', 'CI/CD']),
        ]
        
        for cat_name, skills in categories:
            category, _ = SkillCategory.objects.get_or_create(name=cat_name)
            for skill_name in skills:
                Skill.objects.get_or_create(
                    category=category,
                    name=skill_name,
                    defaults={'proficiency': 80, 'years_experience': 2.0, 'is_active': True}
                )
        self.stdout.write(self.style.SUCCESS('Skills created'))
        
        # Create Blog Categories
        blog_categories = ['AI Engineering', 'Machine Learning', 'Generative AI', 'RAG', 'Agents']
        for name in blog_categories:
            BlogCategory.objects.get_or_create(
                name=name,
                slug=name.lower().replace(' ', '-')
            )
        self.stdout.write(self.style.SUCCESS('Blog categories created'))
        
        self.stdout.write(self.style.SUCCESS('Website initialization complete!'))
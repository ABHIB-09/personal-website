from django.views.generic import TemplateView, FormView, View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from .models import ContactMessage
from .models import ContactMessage, Profile, SocialLink

from .models import (
    Profile,
    ContactMessage,
    WebsiteSettings,
    SocialLink,
    Metric,
    SkillCategory,
)

from .forms import ContactForm


# ============================================================
# HOME PAGE
# ============================================================

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages as django_messages
        from django.shortcuts import redirect

        name         = request.POST.get('name', '').strip()
        email        = request.POST.get('email', '').strip()
        phone        = request.POST.get('phone', '').strip()
        company      = request.POST.get('company', '').strip()
        project_type = request.POST.get('project_type', '').strip()
        message      = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                company=company,
                project_type=project_type,
                message=message,
            )
            django_messages.success(
                request,
                f"Thank you, {name}. Your message has been received. "
                "We will review your enquiry and get back to you at "
                f"{email} within 1–2 business days."
            )
        else:
            django_messages.error(
                request,
                "Please fill in all required fields (Name, Email, and Message)."
            )

        return redirect(request.META.get('HTTP_REFERER', '/') + '#contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ----------------------------------------------------
        # Featured Projects
        # ----------------------------------------------------
        try:
            from portfolio.models import Project

            context['featured_projects'] = (
                Project.objects
                .filter(
                    is_featured=True,
                    is_published=True
                )
                [:6]
            )

        except Exception:
            context['featured_projects'] = []

        # ----------------------------------------------------
        # Recent Blog Posts
        # ----------------------------------------------------
        try:
            from blog.models import BlogPost

            context['recent_posts'] = (
                BlogPost.objects
                .filter(is_published=True)
                [:3]
            )

        except Exception:
            context['recent_posts'] = []

        # ----------------------------------------------------
        # Research Items
        # ----------------------------------------------------
        try:
            from portfolio.models import Research

            context['research_items'] = (
                Research.objects
                .filter(is_published=True)
                [:3]
            )

        except Exception:
            context['research_items'] = []

        # ----------------------------------------------------
        # Experience
        # ----------------------------------------------------
        try:
            from portfolio.models import Experience

            context['experiences'] = (
                Experience.objects
                .filter(is_published=True)
                .order_by('-start_date')
            )

        except Exception:
            context['experiences'] = []

        # ----------------------------------------------------
        # Skills
        # ----------------------------------------------------
        try:
            context['skill_categories'] = (
                SkillCategory.objects
                .filter(is_active=True)
                .prefetch_related('skills')
            )

        except Exception:
            context['skill_categories'] = []

        # ----------------------------------------------------
        # Website Settings
        # ----------------------------------------------------
        try:
            context['website_settings'] = (
                WebsiteSettings.objects.first()
            )

        except Exception:
            context['website_settings'] = None

        # ----------------------------------------------------
        # Profile
        # ----------------------------------------------------
        try:
            context['profile'] = Profile.objects.first()

        except Exception:
            context['profile'] = None

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------
        try:
            context['metrics'] = (
                Metric.objects
                .filter(is_active=True)
            )

        except Exception:
            context['metrics'] = []

        # ----------------------------------------------------
        # Social Links
        # ----------------------------------------------------
        try:
            context['social_links'] = (
                SocialLink.objects
                .filter(is_active=True)
            )

        except Exception:
            context['social_links'] = []

        return context


# ============================================================
# ABOUT PAGE
# ============================================================

class AboutView(TemplateView):
    """
    About / Personal page.
    """

    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['profile'] = Profile.objects.first()

        except Exception:
            context['profile'] = None

        try:
            context['website_settings'] = (
                WebsiteSettings.objects.first()
            )

        except Exception:
            context['website_settings'] = None

        return context


# ============================================================
# CONTACT PAGE
# ============================================================

class ContactView(FormView):
    """
    Contact page with contact form.

    Saves the message to the database and sends
    an email notification to the website owner.
    """

    template_name = 'core/contact.html'

    form_class = ContactForm

    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):

        # ----------------------------------------------------
        # Save contact message
        # ----------------------------------------------------
        message = form.save()

        # ----------------------------------------------------
        # Send email notification
        # ----------------------------------------------------
        try:

            subject = (
                f"New Contact Message from "
                f"{form.cleaned_data['name']}"
            )

            body = render_to_string(
                'core/email_contact_notification.html',
                {
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data['email'],
                    'company': form.cleaned_data.get(
                        'company',
                        ''
                    ),
                    'project_type': form.cleaned_data[
                        'project_type'
                    ],
                    'message': form.cleaned_data['message'],
                }
            )

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.OWNER_EMAIL],
                fail_silently=True,
            )

        except Exception:
            # Do not prevent the contact form from
            # succeeding if email configuration fails.
            pass

        # ----------------------------------------------------
        # Success message
        # ----------------------------------------------------
        messages.success(
            self.request,
            'Thank you for your message! '
            'I will get back to you soon.'
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['profile'] = Profile.objects.first()

        except Exception:
            context['profile'] = None

        try:
            context['website_settings'] = (
                WebsiteSettings.objects.first()
            )

        except Exception:
            context['website_settings'] = None

        return context


# ============================================================
# RESUME
# ============================================================

class ResumeView(View):
    """
    Resume PDF download/view.
    """

    def get(self, request):

        try:

            profile = Profile.objects.first()

            if profile and profile.resume:

                response = FileResponse(
                    profile.resume.open('rb'),
                    content_type='application/pdf'
                )

                response[
                    'Content-Disposition'
                ] = 'inline; filename="resume.pdf"'

                return response

        except Exception:
            pass

        messages.error(
            request,
            'Resume not available.'
        )

        return redirect('core:home')


# ============================================================
# ROBOTS.TXT
# ============================================================

class RobotsView(View):
    """
    robots.txt endpoint.
    """

    def get(self, request):

        content = """User-agent: *
Allow: /

Sitemap: https://your-domain.com/sitemap.xml
"""

        return HttpResponse(
            content,
            content_type='text/plain'
        )


# ============================================================
# SITEMAP
# ============================================================

class SitemapView(View):
    """
    XML sitemap for the website.
    """

    def get(self, request):

        # ----------------------------------------------------
        # Import models locally to avoid circular imports
        # ----------------------------------------------------
        from portfolio.models import Project, Research
        from blog.models import BlogPost

        # ----------------------------------------------------
        # Static Pages
        # ----------------------------------------------------
        class StaticViewSitemap(Sitemap):

            priority = 0.8
            changefreq = 'weekly'

            def items(self):

                return [
                    'core:home',
                    'core:about',
                    'core:contact',
                ]

            def location(self, item):

                return reverse(item)

        # ----------------------------------------------------
        # Projects
        # ----------------------------------------------------
        class ProjectSitemap(Sitemap):

            changefreq = 'monthly'
            priority = 0.9

            def items(self):

                return Project.objects.filter(
                    is_published=True
                )

            def lastmod(self, obj):

                return obj.updated_at

        # ----------------------------------------------------
        # Research
        # ----------------------------------------------------
        class ResearchSitemap(Sitemap):

            changefreq = 'monthly'
            priority = 0.8

            def items(self):

                return Research.objects.filter(
                    is_published=True
                )

            def lastmod(self, obj):

                return obj.updated_at

        # ----------------------------------------------------
        # Blog
        # ----------------------------------------------------
        class BlogSitemap(Sitemap):

            changefreq = 'weekly'
            priority = 0.7

            def items(self):

                return BlogPost.objects.filter(
                    is_published=True
                )

            def lastmod(self, obj):

                return obj.updated_at

        # ----------------------------------------------------
        # Sitemap dictionary
        # ----------------------------------------------------
        sitemaps = {
            'static': StaticViewSitemap,
            'projects': ProjectSitemap,
            'research': ResearchSitemap,
            'blog': BlogSitemap,
        }

        return sitemap(
            request,
            sitemaps
        )

  
def home(request):
    # ---------- Handle Contact Form POST ----------
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip()
        project_type = request.POST.get('project_type', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone or None,
                company=company or None,
                project_type=project_type or '',
                message=message,
            )
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('home')  # or redirect('/#contact')
        else:
            messages.error(request, 'Please fill in all required fields.')

    # ---------- Normal GET request ----------
    context = {
        'profile': Profile.objects.first(),
        'social_links': SocialLink.objects.none(),
        # add your other context variables here (projects, posts, etc.)
    }
    return render(request, 'home.html', context)   # adjust template name if needed


# Add this to core/views.py

from django.views.generic import TemplateView

STATIC_ARTICLES = {
    'gpt6-astra': {
        'title': 'GPT-6 Astra — The Next Evolution of AI',
        'category': 'AI',
        'date': 'Sep 23, 2026',
        'image': 'img/gpt6-astra.png',
        'slug': 'gpt6-astra',
        'content': """
            <p>GPT-6 Astra is pushing AI beyond simple conversations into intelligent action. 
            It can reason through complex problems, use digital tools, interact with computers, 
            and assist with real-world workflows.</p>

            <h2>What makes Astra different?</h2>
            <p>Unlike its predecessors, GPT-6 Astra is designed as an action model — not just a 
            language model. It can browse the web in real time, write and execute code, manage files, 
            call APIs, and coordinate with other AI systems autonomously.</p>

            <h2>Key capabilities</h2>
            <ul>
                <li><strong>Multimodal reasoning</strong> — processes text, images, audio, and video simultaneously</li>
                <li><strong>Tool use</strong> — natively calls external APIs, code interpreters, and search engines</li>
                <li><strong>Long-horizon planning</strong> — breaks complex goals into multi-step execution plans</li>
                <li><strong>Agentic memory</strong> — retains context across sessions for persistent workflows</li>
            </ul>

            <h2>Impact on software engineering</h2>
            <p>From software engineering and business automation to scientific research — the future 
            of AI is about turning intelligence into action. GPT-6 Astra represents a fundamental 
            shift from AI as a tool to AI as a collaborator capable of driving entire workflows 
            with minimal human intervention.</p>

            <h2>What this means for AI engineers</h2>
            <p>The role of the AI engineer is evolving. Instead of prompt engineering alone, 
            the focus shifts to designing reliable agentic pipelines, managing tool orchestration, 
            and building guardrails for autonomous systems that operate in production environments.</p>
        """,
        'read_time': '5 min read',
        'excerpt': 'GPT-6 Astra is pushing AI beyond simple conversations into intelligent action.',
    },
    'ai-robotics': {
        'title': 'AI + Robotics: Transforming the Real World',
        'category': 'AI + Robotics',
        'date': 'Sep 23, 2026',
        'image': 'img/AI_Robotics.png',
        'slug': 'ai-robotics',
        'content': """
            <p>AI + Robotics is creating machines that can sense, learn, decide, and act with 
            minimal human intervention. The convergence of these two fields is producing systems 
            that were science fiction just a decade ago.</p>

            <h2>Where AI meets physical action</h2>
            <p>The real breakthrough comes when AI provides the intelligence and robotics provides 
            the physical action. Large language models now serve as the "brain" of robotic systems, 
            interpreting natural language instructions and translating them into precise motor commands.</p>

            <h2>Key application areas</h2>
            <ul>
                <li><strong>Space exploration</strong> — autonomous rovers that navigate without real-time human control</li>
                <li><strong>Smart farming</strong> — robots that identify crops, detect disease, and harvest autonomously</li>
                <li><strong>Corporate automation</strong> — warehouse robots that adapt to changing layouts in real time</li>
                <li><strong>Healthcare</strong> — surgical robots with AI-guided precision beyond human capability</li>
            </ul>

            <h2>The technical stack powering it</h2>
            <p>Modern AI robotics stacks combine computer vision (OpenCV, YOLO), reinforcement 
            learning, sensor fusion (LiDAR, IMU, cameras), and LLM-based reasoning layers. 
            The result is robots that don't just follow scripts — they reason about their environment.</p>

            <h2>What's next</h2>
            <p>The next frontier is general-purpose robots — machines that can be re-tasked through 
            natural language rather than reprogramming. Companies like Figure, Boston Dynamics, and 
            1X are racing to bring this vision to manufacturing floors and homes.</p>
        """,
        'read_time': '4 min read',
        'excerpt': 'AI + Robotics is creating machines that can sense, learn, decide, and act with minimal human intervention.',
    },
}


class ArticleView(TemplateView):
    template_name = 'core/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        article = STATIC_ARTICLES.get(slug)

        if not article:
            from django.http import Http404
            raise Http404("Article not found")

        context['article'] = article

        try:
            context['profile'] = Profile.objects.first()
        except Exception:
            context['profile'] = None

        try:
            context['social_links'] = SocialLink.objects.filter(is_active=True)
        except Exception:
            context['social_links'] = []

        return context
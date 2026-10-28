from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import HomeView, ArticleView 

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path(
        '3d/', TemplateView.as_view( template_name='core/home_3d.html'), name='home_3d'),

    path(
        'about/', views.AboutView.as_view(), name='about'),

    path(
        'contact/', views.ContactView.as_view(), name='contact'),

    path(
        'resume/', views.ResumeView.as_view(), name='resume'),

    path(
        'robots.txt', views.RobotsView.as_view(), name='robots'),

    path(
        'sitemap.xml', views.SitemapView.as_view(), name='sitemap'),

    path('insights/<slug:slug>/', ArticleView.as_view(), name='article'),
]
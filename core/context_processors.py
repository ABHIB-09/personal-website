from .models import WebsiteSettings, SocialLink, Profile, Metric

def website_settings(request):
    """Context processor for global website settings"""
    try:
        settings = WebsiteSettings.objects.first()
    except:
        settings = None
    
    try:
        profile = Profile.objects.first()
    except:
        profile = None
    
    return {
        'website_settings': settings,
        'profile': profile,
    }

def social_links(request):
    """Context processor for social links"""
    links = SocialLink.objects.filter(is_active=True)
    return {'social_links': links}

def metrics(request):
    """Context processor for metrics"""
    metrics = Metric.objects.filter(is_active=True)
    return {'metrics': metrics}
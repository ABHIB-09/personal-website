// ============================
// Mobile Menu
// ============================
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.getElementById('navLinks');
    
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', function() {
            navLinks.classList.toggle('open');
            mobileToggle.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
        });
    }
    
    // Close mobile menu on link click
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks && navLinks.classList.contains('open')) {
                navLinks.classList.remove('open');
                if (mobileToggle) {
                    mobileToggle.textContent = '☰';
                }
            }
        });
    });
});

// ============================
// Header Scroll Effect
// ============================
const header = document.getElementById('siteHeader');
let lastScroll = 0;

window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    
    if (currentScroll > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// ============================
// Animate Metrics Counters
// ============================
function animateMetrics() {
    const metrics = document.querySelectorAll('.metric-value[data-count]');
    
    if (!metrics.length) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const target = element.getAttribute('data-count');
                const number = parseFloat(target.replace(/[^0-9.]/g, ''));
                
                if (!isNaN(number)) {
                    let current = 0;
                    const increment = Math.ceil(number / 40);
                    const suffix = target.replace(/[0-9.]/g, '');
                    
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= number) {
                            current = number;
                            clearInterval(timer);
                        }
                        element.textContent = current + suffix;
                    }, 30);
                }
                
                observer.unobserve(element);
            }
        });
    }, { threshold: 0.5 });
    
    metrics.forEach(metric => observer.observe(metric));
}

// Wait for page load to animate metrics
if (document.readyState === 'complete') {
    animateMetrics();
} else {
    window.addEventListener('load', animateMetrics);
}

// ============================
// Smooth Scroll for Anchor Links
// ============================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ============================
// Lazy Load Images
// ============================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const src = img.getAttribute('data-src');
                if (src) {
                    img.src = src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ============================
// Video Lazy Loading
// ============================
document.querySelectorAll('.video-container[data-video-url]').forEach(container => {
    const poster = container.querySelector('.video-poster');
    const playBtn = container.querySelector('.play-button');
    const videoUrl = container.getAttribute('data-video-url');
    
    if (playBtn && videoUrl) {
        playBtn.addEventListener('click', function() {
            const iframe = document.createElement('iframe');
            iframe.src = videoUrl;
            iframe.width = '100%';
            iframe.height = '100%';
            iframe.style.border = 'none';
            iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
            iframe.allowFullscreen = true;
            
            container.innerHTML = '';
            container.appendChild(iframe);
        });
    }
});

// ============================
// Copy to Clipboard
// ============================
document.querySelectorAll('[data-copy]').forEach(element => {
    element.addEventListener('click', function(e) {
        const text = this.getAttribute('data-copy');
        if (text) {
            navigator.clipboard.writeText(text).then(() => {
                const originalText = this.textContent;
                this.textContent = '✓ Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            });
        }
    });
});

// ============================
// Form Validation
// ============================
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const required = this.querySelectorAll('[required]');
        let valid = true;
        
        required.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });
        
        if (!valid) {
            e.preventDefault();
            const firstError = this.querySelector('.error');
            if (firstError) {
                firstError.focus();
            }
        }
    });
});

// ============================
// Reduce Motion
// ============================
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (prefersReducedMotion.matches) {
    document.querySelectorAll('.ai-flow-item').forEach(item => {
        item.style.animation = 'none';
        item.style.opacity = '1';
        item.style.transform = 'translateX(0)';
    });
}

// ============================
// CMS: Confirm Delete
// ============================
document.querySelectorAll('.confirm-delete').forEach(link => {
    link.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to delete this?')) {
            e.preventDefault();
        }
    });
});

// ============================
// CMS: Toggle Publish
// ============================
document.querySelectorAll('.toggle-publish').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const url = this.getAttribute('data-url');
        const statusBadge = this.closest('tr').querySelector('.status-badge');
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.is_published) {
                    statusBadge.textContent = 'Published';
                    statusBadge.className = 'status-badge published';
                    this.textContent = 'Unpublish';
                } else {
                    statusBadge.textContent = 'Draft';
                    statusBadge.className = 'status-badge draft';
                    this.textContent = 'Publish';
                }
            }
        });
    });
});

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ============================
// Console greeting
// ============================
console.log('%c👋 Hey there!', 'font-size: 24px; font-weight: bold; color: #3182ce;');
console.log('%cThanks for checking out my portfolio. Feel free to reach out!', 'font-size: 14px; color: #4a5568;');
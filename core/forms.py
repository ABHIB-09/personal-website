from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Contact form"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'project_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
                'required': True,
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Company name (optional)',
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }, choices=[
                ('', 'Select project type...'),
                ('AI/ML', 'AI/Machine Learning'),
                ('Generative AI', 'Generative AI'),
                ('RAG', 'RAG Systems'),
                ('AI Agents', 'AI Agents'),
                ('Automation', 'Automation'),
                ('Computer Vision', 'Computer Vision'),
                ('Consulting', 'Consulting'),
                ('Other', 'Other'),
            ]),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 6,
                'placeholder': 'Tell me about your project...',
                'required': True,
            }),
        }
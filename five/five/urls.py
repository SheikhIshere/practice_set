"""
URL configuration for five project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('task/', include('task.urls')),
    path('', index, name='homepage'),

    # other pages
    path('features/', TemplateView.as_view(template_name='other_page/Features.html'), name='features'),
    path('pricing/', TemplateView.as_view(template_name='other_page/Pricing.html'), name='pricing'),
    path('integrations/', TemplateView.as_view(template_name='other_page/Integrations.html'), name='integrations'),
    path('updates/', TemplateView.as_view(template_name='other_page/Updates.html'), name='updates'),
    path('documentation/', TemplateView.as_view(template_name='other_page/Documentation.html'), name='documentation'),
    path('tutorials/', TemplateView.as_view(template_name='other_page/Tutorials.html'), name='tutorials'),
    path('blog/', TemplateView.as_view(template_name='other_page/Blog.html'), name='blog'),
    path('support/', TemplateView.as_view(template_name='other_page/Support.html'), name='support'),
    path('about-us/', TemplateView.as_view(template_name='other_page/AboutUs.html'), name='about-us'),
    path('careers/', TemplateView.as_view(template_name='other_page/Careers.html'), name='careers'),
    path('contact/', TemplateView.as_view(template_name='other_page/Contact.html'), name='contact'),
    path('partners/', TemplateView.as_view(template_name='other_page/Partners.html'), name='partners'),
]

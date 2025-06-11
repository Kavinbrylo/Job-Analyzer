from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape/', views.scrape_jobs, name='scrape_jobs'),
    path('analyze/', views.analyze_jobs, name='analyze_jobs'),
]
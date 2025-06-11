from django.shortcuts import render
from .models import Job
import pandas as pd
import matplotlib.pyplot as plt
import os

# Home Page
def home(request):
    query = request.GET.get('q')
    if query:
        jobs = job.objetcs.fliter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'jobs/home.html', {'jobs': jobs})

# Scraping with Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_jobs(request):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.indeed.com/jobs?q=python+developer&l=")
    time.sleep(3)

    Job.objects.all().delete()
    job_cards = driver.find_elements(By.CLASS_NAME, 'result')[:10]  # Top 10 jobs

    for card in job_cards:
        title = card.find_element(By.CLASS_NAME, 'jobTitle').text
        company = card.find_element(By.CLASS_NAME, 'companyName').text
        location = card.find_element(By.CLASS_NAME, 'companyLocation').text
        summary = card.find_element(By.CLASS_NAME, 'job-snippet').text
        date_posted = card.find_element(By.CLASS_NAME, 'date').text
        Job.objects.create(title=title, company=company, location=location, summary=summary, date_posted=date_posted)

    driver.quit()
    return render(request, 'jobs/scrape_done.html')

# Analysis
def analyze_jobs(request):
    jobs = Job.objects.all()
    df = pd.DataFrame(list(jobs.values()))

    if not os.path.exists('jobs/static/charts'):
        os.makedirs('jobs/static/charts')

    # Location Chart
    plt.figure(figsize=(6, 4))
    df['location'].value_counts().head(5).plot(kind='bar')
    plt.title('Top Job Locations')
    plt.savefig('jobs/static/charts/location_chart.png')
    plt.close()

    # Company Chart
    plt.figure(figsize=(6, 4))
    df['company'].value_counts().head(5).plot(kind='bar', color='orange')
    plt.title('Top Hiring Companies')
    plt.savefig('jobs/static/charts/company_chart.png')
    plt.close()

    return render(request, 'jobs/analyze.html', {
        'chart': '/static/charts/location_chart.png',
        'chart2': '/static/charts/company_chart.png'
    })

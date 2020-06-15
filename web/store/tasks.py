import requests
from celery import task
from django.conf import settings
from store.models import Rating


@task
def fit_model():
    fit_url = settings.FIT_URL
    rate_counts = Rating.objects.all().count()
    if rate_counts % 2 == 0:
        try:
            requests.get(fit_url)
        except requests.ConnectionError:
            print('Can not send request.')
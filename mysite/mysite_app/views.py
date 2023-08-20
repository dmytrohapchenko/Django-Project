from django.shortcuts import render
from .functions import get_hackernews_data, get_news24_data, get_hackspace_data


def home(request):
    context = {
        'hackernews_list': get_hackernews_data()[:9],
        'news24__list': get_news24_data()[:9],
        'hackspace_list': get_hackspace_data()[:9],
    }
    return render(request, 'mysite_app/home.html', context)

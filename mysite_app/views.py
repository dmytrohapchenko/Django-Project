from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.
# Сайти для парсинга


hackernews_url = 'https://thehackernews.com/'
news24_url = 'https://24tv.ua/golovni-novini_tag1792/'
hackspace_url = 'https://hackspace.raspberrypi.org/articles'


hackernews_list = []
news24__list = []
hackspace_list = []


def get_hackernews():
    r = requests.get(hackernews_url).text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all('div', class_='body-post clear')
    for post in posts:
        img = post.find('img')
        src = img.get('data-src')
        label = post.find('div', class_='item-label').text
        label = label[2:-1]
        title = post.find('h2', class_='home-title').text
        desc = post.find('div', class_='home-desc').text
        desc = desc[:200] + '...'
        url = post.find('a').get('href')

        data = {
            'src': src,
            'label': label,
            'title':title,
            'desc':desc,
            'url':url,
            }
        hackernews_list.append(data)


def get_news24():
    r = requests.get(news24_url).text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all('app-news-item')
    for post in posts:
        title = post.find('h3', class_='news-title').text
        span = post.find('span').text
        post_views = post.find('div', class_='news-views').text
        url = post.find('a').get('href')

        t_r = requests.get(url).text
        t_soup = BeautifulSoup(t_r, 'lxml')
        img = t_soup.find('img', class_="main-news-photo")
        src = img.get('src')
        t_desc = t_soup.find('p', class_="news-annotation").text

        data = {
            'src':src,
            'title':title,
            't_desc':t_desc,
            'span':span,
            'post_views':post_views,
            'url':url,
            }
        news24__list.append(data)


def get_hackspace():
    r = requests.get(hackspace_url).text
    soup = BeautifulSoup(r, "lxml")
    posts = soup.find_all("article")
    for post in posts:
        img = post.find('img')
        src = img.get('src')
        title = post.find("p", class_="o-type-sub-heading u-weight-bold rspec-article-card--heading").text
        time = post.find('time').text
        url = post.find("a").get("href")

        t_r = requests.get(url).text
        t_soup = BeautifulSoup(t_r, 'lxml')
        desc = t_soup.find('div', class_="c-wysiwyg rspec-article-introduction").text
        if len(desc) > 200:
            desc = desc[:200] + '...'
        else:
            continue
        
        data = {
                'src': src,
                'title': title,
                'time':time,
                'desc':desc,
                'url': url,
                }

        hackspace_list.append(data)

get_hackernews()
get_news24()
get_hackspace()

hackernews_list = hackernews_list[:9]
news24__list = news24__list[:9]
hackspace_list = hackspace_list[:9]

# Для відображення сторінки html
def home(request):
    context = {
        'hackernews_list':hackernews_list,
        'news24__list':news24__list,
        'hackspace_list': hackspace_list,
    }
    return render(request, 'mysite_app/home.html', context)
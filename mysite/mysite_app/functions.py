from bs4 import BeautifulSoup
import requests


def get_hackernews_data():
    data_list = []
    r = requests.get('https://thehackernews.com/').text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all(class_='body-post clear')
    for post in posts:
        src = (post.find('img')).get('data-src')
        label = post.find(class_='item-label').text[2:-1]
        title = post.find(class_='home-title').text
        desc = post.find(class_='home-desc').text[:200] + '...'
        url = post.find('a').get('href')

        data = {
            'src': src,
            'label': label,
            'title': title,
            'desc': desc,
            'url': url,
        }
        data_list.append(data)
    return data_list


def get_news24_data():
    data_list = []
    r = requests.get('https://24tv.ua/golovni-novini_tag1792/').text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all('app-news-item')
    for post in posts:
        title = post.find(class_='news-title').text
        span = post.find('span').text
        post_views = post.find(class_='news-views').text
        url = post.find('a').get('href')

        t_r = requests.get(url).text
        t_soup = BeautifulSoup(t_r, 'lxml')
        src = (t_soup.find(class_="main-news-photo")).get('src')
        t_desc = t_soup.find(class_="news-annotation").text

        data = {
            'src': src,
            'title': title,
            't_desc': t_desc,
            'span': span,
            'post_views': post_views,
            'url': url,
        }
        data_list.append(data)
    return data_list


def get_hackspace_data():
    data_list = []
    r = requests.get('https://hackspace.raspberrypi.org/articles').text
    soup = BeautifulSoup(r, "lxml")
    posts = soup.find_all("article")
    for post in posts:
        src = (post.find('img')).get('src')
        title = post.find(class_="o-type-sub-heading u-weight-bold rspec-article-card--heading").text
        time = post.find('time').text
        url = post.find("a").get("href")

        t_r = requests.get(url).text
        t_soup = BeautifulSoup(t_r, 'lxml')
        desc = t_soup.find(class_="c-wysiwyg rspec-article-introduction").text
        if len(desc) > 200:
            desc = desc[:200] + '...'
        else:
            continue

        data = {
            'src': src,
            'title': title,
            'time': time,
            'desc': desc,
            'url': url,
        }

        data_list.append(data)
    return data_list

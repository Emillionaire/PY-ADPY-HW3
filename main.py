import requests
import bs4
import re

HEADERS = {
    'Host': 'habr.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://github.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1'
}
KEYWORDS = {'программист', 'фото', 'сейчас', 'python', 'для'}
site_href = 'https://habr.com'

response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
all_posts = soup.find_all(id=range(600000, 700000))
for post in all_posts:
    #check keywords
    post_text = str(post.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2'))
    pull_keys = []
    for key in KEYWORDS:
        request = f'(?i)\\b{key}\\b'
        try:
            request_answer = re.search(request, post_text).group(0)
            pull_keys.append(request_answer)
        except AttributeError:
            continue
    if KEYWORDS & set(pull_keys):
        # find title
        title = post.find('div').find('h2').find('a').find('span').text
        # find date and time
        raw_date = str(post.find('time'))
        result_date = re.search(r'title=\"(.*), (.*)\"', raw_date)
        date = result_date.group(1)
        time = result_date.group(2)
        # find link
        raw_link = str(post.find(class_='tm-article-snippet__title-link'))
        result_link = re.search(r'href=\"(.*)\"', raw_link)
        link = site_href + result_link.group(1)
        # print result
        print(f'{date} - {time} - {title} - {link}')

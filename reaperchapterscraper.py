import os
import requests
import urllib.request
from bs4 import BeautifulSoup

def chapdown(chapter_url, series_path):
    website = chapter_url

    bs = BeautifulSoup(requests.get(website).text, 'html.parser')

    #folder naming
    header = bs.find('h1', {"id": "chapter-heading"})
    ch_title = header.text.strip()
    print(ch_title)

    chapter_path = os.path.join(series_path, ch_title).replace("\\","/")
    if os.path.exists(chapter_path):
        pass
    else:
        os.mkdir(chapter_path)

    images = bs.find_all('img', {"class": "wp-manga-chapter-img"})

    url_list = []

    for img in images:
        if img.has_attr('data-src'):
            url_list.append(img['data-src'].strip())

    # for x in url_list:
    #     print(x)

    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')

    counter = -1
    os.chdir(chapter_path)
    for url in url_list:
        counter += 1
        filename = str(counter) + ".jpg"
        opener.retrieve(url, filename)
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")
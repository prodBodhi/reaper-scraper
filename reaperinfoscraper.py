import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
from reaperchapterscraper import chapdown

curDir, _ = os.path.split(os.path.abspath(__file__))

series_path = os.path.join("./", "series")
if os.path.exists(series_path):
    pass
else:
    os.mkdir(series_path)

website = input("Enter Reaper Scans series page link: ")

bs = BeautifulSoup(requests.get(website).text, 'html.parser')

all_information = ""

series_release = bs.find_all('div', {"class": "post-content_item"}) #Finds all information, including heading and content
a_list = []
for x in series_release:
    a_list.append(x.text.replace("\n", "").strip()) #Adds all information to a list
a_list.pop(0) #Removes title from list
a_list.pop(0) #Removes ranking from list

series_name = bs.find('h1', {"style": "margin-bottom:5px;"}) #Finds title
name = series_name.text.strip()
all_information = 'Title: ' + name #Prints title

latest_chapter = bs.find_all('p', {"class": "chapter-manhwa-title"}) #Finds latest chapter
b_list = []
for x in latest_chapter:
    b_list.append(x.text.replace("\n", "").strip()) #Adds all information to a list
all_information += '\nLatest Chapter: ' + b_list[0] #Prints latest chapter
total_chap = int("".join(filter(str.isdigit, b_list[0])))

images = bs.find('img', {"style": "padding-top:395px;"})
if images.has_attr('data-src'):
    image_url = images['data-src'].strip()
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')

def insert_colon(string, index): #Adds colon between heading and content
    return string[:index] + ':' + string[index:]

for x in a_list: #Runs insert_colon to all indices
    if 'Alternative' in x:
        new_x = insert_colon(x, 11)
        all_information += '\n' + new_x
    if 'Author(s)' in x:
        new_x = insert_colon(x, 9)
        all_information += '\n' + new_x
    if 'Artist(s)' in x:
        new_x = insert_colon(x, 9)
        all_information += '\n' + new_x
    if 'Genre(s)' in x:
        new_x = insert_colon(x, 8)
        all_information += '\n' + new_x
    if 'Type' in x:
        new_x = insert_colon(x, 4)
        all_information += '\n' + new_x
    if 'Release' in x:
        new_x = insert_colon(x, 7)
        all_information += '\n' + new_x
    if 'Status' in x:
        new_x = insert_colon(x, 6)
        all_information += '\n' + new_x

name_path = os.path.join('./series/', re.sub('[^a-zA-Z0-9 \n\.]', '', name))
print('NAME PATH: ' + name_path)
if os.path.exists(name_path):
    pass
else:
    os.mkdir(name_path)

os.chdir(name_path)
print('CURRENT DIR: ' + curDir)
opener.retrieve(image_url, 'cover' + ".jpg")
with open('series-info.txt', 'w', encoding='utf-8') as f:
    f.write(all_information)

os.chdir("..")
print('CURRENT DIR: ' + curDir)
os.chdir("..")
print('CURRENT DIR: ' + curDir)
i = 1
while i <= total_chap:
    print('CURRENT i' + str(i))
    chapdown(website + 'chapter-' + str(i), name_path)
    i = i+1

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
import json
from bs4 import BeautifulSoup


def get_phone_url(pid):
    return 'https://www.miui.com/download-' + str(pid) + '.html'


def get_cate():
    url = 'https://www.miui.com/download.html'
    r = requests.get(url)
    text = r.text
    json_str = re.findall(r'phones =(.*?);', text, re.S)[0]
    dict_phones = json.loads(json_str)
    list = []
    for phone in dict_phones:
        pid = phone['pid']
        name = phone['name']
        pic = phone['pic']
        phone_url = get_phone_url(pid)
        dict = {'name': name, 'pid': pid, 'pic': pic, 'phone_url': phone_url}
        list.append(dict)
    return json.dumps(list)


def get_phone_info(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    phone = soup.find('div', class_='phone_hd').span.string
    dict_phone = {'phone': phone, 'info': []}
    contents = soup.find_all('div', class_='block')
    for content in contents:
        soup2 = BeautifulSoup(str(content), 'html.parser')
        title = soup2.h2.string
        rom_url = soup2.find('div', class_='to_miroute').a['href']
        infos = soup2.find_all('div', class_='supports')[0].p.contents
        author = infos[0]
        version = str(infos[2]).strip()
        size = infos[4]
        other = author + ' ' + version + ' ' + size
        dict_info = {'title': title, 'rom_url': rom_url, 'other': other}
        dict_phone['info'].append(dict_info)
    return json.dumps(dict_phone)


if __name__ == '__main__':


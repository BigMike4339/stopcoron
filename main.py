#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

DEBUG = False
true = True
false = False


def get_data_from_site(url: str):
    r = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    print("Get html")
    try:
        r = requests.get(url, headers=headers)
    except Exception as err:
        print(f"Error on request: {err}")

    return r.text


def new_date(soup) -> bool:
    rv: bool = True

    #_date = soup.find('h1', {'class': 'cv-section__title cv-section__title_mobile-small'})

    return rv


def parse_new_data(soup):

    print("Parse")

    #data_soup = soup.find('div', {'class': 'cv-section__content'})
    data_soup = soup.find('section', {'class': 'cv-section'})

    #date = data_soup.find('h1', {'class': 'cv-section__title cv-section__title_mobile-small'})

    data_soup_child = data_soup.find('div', {'class': 'cv-section__content'})
    #print(data_soup_child.contents[7].attrs[":charts-data"])
    #exit()

    new_data = data_soup_child.contents[7].attrs[":charts-data"]
    exec(f"__new_data = {new_data}", globals())
    _new_data = __new_data

    data_soup = soup.find('section', {'class': 'cv-section'}).find_next_sibling()

    data_soup_child = data_soup.find('div', {'class': 'cv-section__content'})
        
    #print(data_soup_child.contents[3].attrs[":spread-data"])
    #exit()

    new_data = data_soup_child.contents[3].attrs[":spread-data"]
    new_data = re.sub('null', 'None', new_data)
    #print(type(new_data))
    #print(new_data)
    #exit()

    exec(f"__new_data = {new_data}", globals())
    _new_data1 = __new_data

    # date.contents[2].contents[0],
    return {
        "date": _new_data[0]["date"],
        "ru_sick": _new_data[0]["sick"], "ru_healed": _new_data[0]["healed"], "ru_man_died":_new_data[0]["died"],
        "msk_sick": _new_data1[0]["sick"], "msk_healed": _new_data1[0]["healed"], "msk_man_died":_new_data1[0]["died"]
    }


# ==============================================
if __name__ == '__main__':

    if DEBUG:
        with open('test.html', 'r') as input_file:
            page = input_file.read()
    else:
        url = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/information/'
        page = get_data_from_site(url)

        #if DEBUG:
        #    with open('test.html', 'w') as output_file:
        #        output_file.write(page)

    soup = BeautifulSoup(page, features="lxml")
    if new_date(soup):
        info = parse_new_data(soup)
        #(cases_identified, man_died, cases_identified_moscow)

        pprint(info)
        print()

    wait = input("Press Enter to exit")

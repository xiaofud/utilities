#!/usr/bin/env python3
# coding=utf-8
__author__ = 'smallfly'

import requests
from bs4 import BeautifulSoup

NEWS_ADDRESS = "https://ielts.etest.net.cn/allnews"

class NewsItem:

    def __init__(self, date, title, url):
        self.__data = {
            "date": date,
            "title": title,
            "url": url
        }

    def __repr__(self):
        return repr(self.__data)

    def __getattr__(self, item):
        if item in self.__data:
            return self.__data[item]
        raise AttributeError("NewsItem has no attribute named {}.".format(item))


def get_raw_news(address):
    resp = requests.get(address)
    if resp.ok:
        resp.encoding = "UTF-8"
        return resp.text
    else:
        return None

def parse_news(content):
    soup = BeautifulSoup(content)
    all_news_li = soup.find_all("li", {"class": "main-sub-act-new"})
    news_items = []
    for li in all_news_li:
        # 存有新闻链接a标签的span标签
        span_with_a_tag = li.contents[0]
        # 存有发布时间的span标签
        span_with_date = li.contents[1]
        # 存放新闻链接的a标签
        a_tag = span_with_a_tag.a
        date_string = span_with_date.string.strip()
        news_items.append(NewsItem(date_string[1: len(date_string) - 1], a_tag.string.strip(), a_tag["href"]))
        # print(span_with_date.string.strip(), a_tag.string, a_tag["href"])
    return news_items

def pretty_print(items):
    items.sort(key=lambda x: x.date, reverse=True)
    for item in items:
        print("Date:", item.date)
        print("Title:", item.title)
        print("URL:", item.url)
        print()

if __name__ == "__main__":
    content = get_raw_news(NEWS_ADDRESS)
    if content is not None:
        items = parse_news(content)
        pretty_print(items)
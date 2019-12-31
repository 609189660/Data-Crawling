from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy import Spider, FormRequest
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
import re
from time import sleep
from random import randint
import pandas as pd
from pymongo import MongoClient
import random
from selenium.webdriver.common.keys import Keys
from collections import Counter
from collections import defaultdict
from datetime import datetime
import numpy as np
import random

# def read_csv():
#     file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/enginelist.csv'
#     df=pd.read_csv(file_location)
#     enginelist=df['engine'].tolist()
#     return enginelist,df

# enginelist,df=read_csv()
# # print(enginelist)

def get_key_word():##get the key word we'll use to search from MongoDB
    client = MongoClient('mongodb://localhost:27017')
    result = client.ebay.key_word.find({})
    key_word = [page_dict['key_word'] for page_dict in result]
    return key_word


def filter_out_scrapied_key_word(key_word):#filter the engine
    client = MongoClient('mongodb://localhost:27017')
    result = client.ebay.html_page.find({})
    searched_key_word = [page_dict['key_word'] for page_dict in result]

    not_searched_key_word = []
    for key_word in key_word:
        if key_word not in searched_key_word:
            not_searched_key_word.append(key_word)
        else:
            print(key_word)
            continue
    return not_searched_key_word

def search_key_word(driver,key_word):
    driver.find_element_by_id('gh-ac').clear()
    sleep(randint(5, 10))
    driver.find_element_by_id('gh-ac').send_keys(key_word)
    sleep(randint(5, 10))
    driver.find_element_by_id('gh-btn').click()


def save_html_source(key_word,html):
    client = MongoClient('mongodb://localhost:27017')
    page_dict = dict()
    page_dict['key_word'] = key_word
    page_dict['html'] = html

    client.ebay.html_page.insert_one(page_dict)##save the html url in the dic
    client.close()

class safetyspider(Spider):
    name = "ebay"
    count = 0
    def start_requests(self):
        file_location = 'C:/Users/Server/Downloads/chromedriver_win32/chromedriver.exe'
        # total_searched_itmes = 0
        self.driver = webdriver.Chrome(file_location)
        # self.driver.maximize_window()
        # self.driver.set_window_size(2000,2500)
        # global base_url
        # tag = 'rareelectrical_generator_search_page'
        # self.driver.get(base_url)
        sleep(5)


        self.driver.get('https://www.ebay.com/')
        sleep(randint(5, 10))


        key_word=get_key_word()

        key_word = filter_out_scrapied_key_word(key_word)
        for key_word in key_word:
            search_key_word(self.driver,key_word)
            sleep(randint(5, 10))
            html=self.driver.page_source

            save_html_source(key_word, html)
            print("save success: "+key_word)
            self.count = self.count + 1
            print('total scrapied item:' + str(self.count))
            # if self.count >= 30:
            #     raise scrapy.exceptions.CloseSpider('------end of scrapy')
            sleep(randint(60,120))

        raise scrapy.exceptions.CloseSpider('------end of scrapy')


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

# file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/chromedriver.exe'
# driver = webdriver.Chrome(file_location)

def convert_ebaypage_to_info(html,item_search):
    result_list = []
    sel = Selector(text=html)

    # frame = driver.find_element_by_name('resultsFrame')
    # driver.switch_to_frame(frame)

    li = sel.xpath(".//div[@id='srp-river-results']//li[@class='s-item   ']")

    for i in range(len(li)):

        # if li[i].xpath(".//span[@class='s-snihwk']/text()").extract():
        #     sponsorship=['sponsored']
        # else:
        #     sponsorship=[]
        # print(sponsorship)
        # print(len(li[i].xpath("//span[@role='text']/span/text()")))
        # print(li[i].xpath("//div[@class='s-item__title--tagblock']/span[@role='text']/span[@class='s-snihwk']/text()"))

        if any('Sold' in s for s in li[i].xpath(".//span[@class='BOLD NEGATIVE']/text()").extract()):
            amount_sold = li[i].xpath(".//span[@class='BOLD NEGATIVE']/text()").extract()
        else:
            amount_sold=[]

        img=li[i].xpath(".//img/@src").extract()
        # print(img)
        item_title = li[i].xpath(".//h3/text()").extract()
        # print(item_title)

        New_or_Used=li[i].xpath(".//span[@class='SECONDARY_INFO']/text()").extract()
        # print(New_or_Used)

        price = li[i].xpath(".//span[@class='s-item__price']/text()").extract()
        # print(price)

        price_was=li[i].xpath(".//span[@class='STRIKETHROUGH']/text()").extract()
        # print(price_was)




        Ship_Return_Sale=li[i].xpath(".//span[@class='BOLD']/text()").extract()
    # print(Ship_Return_Sale)
    # print('')



        row_dict = dict()
        # row_dict['sponsorship'] = ','.join(sponsorship)
        row_dict['img'] = ','.join(img)
        row_dict['item_search']=item_search
        row_dict['item_title'] = ','.join(item_title)
        row_dict['New_or_Used'] = ','.join(New_or_Used)
        row_dict['price'] = ','.join(price)
        row_dict['price_was'] = ','.join(price_was)
        row_dict['amount_sold'] = ','.join(amount_sold)
        row_dict['Ship_Return_Sale'] = ','.join(Ship_Return_Sale)
        result_list.append(row_dict)


    return result_list



def read_html_from_db():
    client = MongoClient('mongodb://localhost:27017')
    result = client.ebay.html_page.find({})

    saved_html = [page_dict['html'] for page_dict in result]
    return saved_html

def get_engine_code():
    client = MongoClient('mongodb://localhost:27017')
    result = client.ebay.html_page.find({})

    engine_code = [page_dict['engine_code'] for page_dict in result]

    return  engine_code

# #codes below can get all the products listed on the ebay search result page##
# result_list = []
# for i in range(len(read_html_from_db())):
#         html=read_html_from_db()[i]
#         engine_code=get_engine_code()[i]
#         engine_list = convert_safety_to_get_engine_num_and_informatin(html,engine_code)
#         result_list.extend(engine_list)
#
# df = pd.DataFrame(result_list)
# df.to_csv( 'car_make.csv')



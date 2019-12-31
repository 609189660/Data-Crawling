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

def convert_kit_page_to_csv(html,kit):
    result_list = []
    sel = Selector(text=html)

    # frame = driver.find_element_by_name('resultsFrame')
    # driver.switch_to_frame(frame)

    tablerows = sel.xpath('.//tbody[1]/tr')

    for i in range(2,len(tablerows)):

        kit_number = sel.xpath('//tbody/tr[1]/td/text()').extract()[1]
        # print(kit_number)




        Safety=sel.xpath('//td[1]/text()').extract()[i]
        print(Safety)

        Qty=sel.xpath('//td[2]/text()').extract()[i]


        if sel.xpath('//tr[{}]/td[3]/text()'.format(i+1)).extract_first() is None:
            Description=''
        else:
            Description = sel.xpath('//tr[{}]/td[3]/text()'.format(i+1)).extract_first()

        if sel.xpath('//tr[{}]/td[4]/text()'.format(i + 1)).extract_first() is None:
            Specifications = ''
        else:
            Specifications = sel.xpath('//tr[{}]/td[4]/text()'.format(i + 1)).extract_first()


        row_dict = dict()
        row_dict['kit'] = kit
        row_dict['kit_number'] = kit_number
        row_dict['Safety'] = Safety
        row_dict['Qty'] = Qty
        row_dict['Description'] = Description
        row_dict['Specifications'] = Specifications
        result_list.append(row_dict)
        # save_to_mongodb(row_dict)

    return result_list


def read_html_from_db():
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.kit_page.find({})

    saved_html = [page_dict['html'] for page_dict in result]
    return saved_html

def get_kit():
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.kit_page.find({})

    kit = [page_dict['kit'] for page_dict in result]


    return  kit


# result_list = []
# for i in range(len(read_html_from_db())):
#         html=read_html_from_db()[i]
#         kit=get_kit()[i]
#         kit_list=convert_kit_page_to_csv(html,kit)
#         result_list.extend(kit_list)
# df = pd.DataFrame(result_list)
# df.to_csv('kit.csv')


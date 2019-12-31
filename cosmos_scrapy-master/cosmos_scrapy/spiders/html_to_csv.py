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

def convert_safety_to_get_engine_num_and_informatin(html,engine_code):
    result_list = []
    sel = Selector(text=html)

    # frame = driver.find_element_by_name('resultsFrame')
    # driver.switch_to_frame(frame)

    tablerows = sel.xpath('.//tbody[1]/tr')


    for i in range(3,len(tablerows)-1):

        engine_number = sel.xpath('//tbody/tr[1]/td/text()').extract()[0]
        # print(engine_number)
        car_year_model = sel.xpath('//tbody/tr[2]/td/text()').extract()
        # print(car_year_model)

        if sel.xpath('//tr[{}]/td[1]/text()'.format(i + 1)).extract_first() is None:
            Part_Type = 'no name'
        else:
            Part_Type=sel.xpath('//tr[{}]/td[1]/text()'.format(i + 1)).extract_first()

        # print(Part_Type)





        if len(sel.xpath('//tr[{}]/td/text()'.format(i+1)).extract())==1:
            Safety='n/a'
            notes='group name'
            temp=Part_Type ##save the group name

        else:
            Safety=str('z'+sel.xpath('//tr[{}]/td/text()'.format(i+1)).extract()[1])
            notes=temp


        status = ''

        # print(sel.xpath('//tr[{}]/td[2]/@class'.format(i+1)).extract_first())
        if sel.xpath('//tr[{}]/td[2]/@class'.format(i+1)).extract_first() == 'tdTBD':
            status = 'In Development'

        elif sel.xpath('//tr[{}]/td[2]/@class'.format(i+1)).extract_first() == 'tdNA':
            status = 'Currently Unavailable'

        else:
            status = 'Part Available'


        if sel.xpath('//tr[{}]/td[3]/text()'.format(i+1)).extract_first() is None:
            Comments1=''
        else:
            Comments1 = 'notes:'+ sel.xpath('//tr[{}]/td[3]/text()'.format(i+1)).extract_first()

        if sel.xpath('//tr[{}]/td[4]/text()'.format(i + 1)).extract_first() is None:
            Comments2 = ''
        else:
            Comments2 = 'notes:'+ sel.xpath('//tr[{}]/td[4]/text()'.format(i + 1)).extract_first()


        row_dict = dict()
        row_dict['Part_Type'] = Part_Type
        row_dict['Safety'] = str(Safety)
        row_dict['Comments1'] = Comments1
        row_dict['Comments2'] = Comments2
        row_dict['engine_number'] = engine_number
        row_dict['car_year_model'] = ','.join(car_year_model)
        row_dict['notes']=notes
        row_dict['status'] = status
        row_dict['engine_code']=engine_code
        result_list.append(row_dict)
        # save_to_mongodb(row_dict)

    # df = pd.DataFrame(result_list)
    # df.to_csv( 'car_make.csv')
    return result_list
    # df.to_csv('~/Desktop/' + 'car_make' + '.csv')


def read_html_from_db():
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.html_page.find({})

    saved_html = [page_dict['html'] for page_dict in result]
    return saved_html

def get_engine_code():
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.html_page.find({})

    engine_code = [page_dict['engine_code'] for page_dict in result]

    return  engine_code

# result_list = []
# for i in range(178,179):
#         html=read_html_from_db()[i]
#         engine_code=get_engine_code()[i]
#         if engine_code=='MAZ-MZI':
#             print(i)
#         engine_list = convert_safety_to_get_engine_num_and_informatin(html,engine_code)
#         result_list.extend(engine_list)
# df = pd.DataFrame(result_list)
# df.to_csv( 'car_make4.csv')




# result_list = []
# for i in range(536):
#         html=read_html_from_db()[i]
#         engine_code=get_engine_code()[i]
#         engine_list = convert_safety_to_get_engine_num_and_informatin(html,engine_code)
#         result_list.extend(engine_list)
#         print(i)
# for i in range(537,669):
#         html=read_html_from_db()[i]
#         engine_code=get_engine_code()[i]
#         engine_list = convert_safety_to_get_engine_num_and_informatin(html,engine_code)
#         result_list.extend(engine_list)
#         print(i)
# for i in range(670,len(read_html_from_db())):
#         html=read_html_from_db()[i]
#         engine_code=get_engine_code()[i]
#         engine_list = convert_safety_to_get_engine_num_and_informatin(html,engine_code)
#         result_list.extend(engine_list)
#         print(i)
# df = pd.DataFrame(result_list)
# df.to_csv( 'car_make3.csv')

# print(get_engine_code()[669])

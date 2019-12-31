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
import codecs

# file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/chromedriver.exe'
# driver = webdriver.Chrome(file_location)


def convert_safety_to_get_engine_num_and_informatin(kit,html_location):
    result_list = []
    sel = Selector(text=codecs.open(html_location, 'r').read())
    options = sel.xpath('.//option')
    for i in range(len(options)):
        # print i
        kit_number = options[i].xpath('//option/text()').extract()[i]

        row_dict = dict()
        row_dict['kit'] = kit
        row_dict['kit_number'] = kit_number
        result_list.append(row_dict)

    df = pd.DataFrame(result_list)
    df.to_csv('~/Desktop/'+ kit + '.csv')

# html_location = 'kit1.html'
# kit ='(SECK) Complete Engine Kit'
# convert_safety_to_get_engine_num_and_informatin(kit,html_location)




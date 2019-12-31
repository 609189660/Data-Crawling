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



def csv_to_db():
    client = MongoClient('mongodb://localhost:27017')

    file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/key_word.csv'
    df=pd.read_csv(file_location)
    key_word=df['Exhaust Valve'].tolist()
    notes=df['notes'].tolist()
    for i in range(len(key_word)):
        page_dict = dict()
        page_dict['key_word'] = key_word[i]
        page_dict['notes']=notes[i]
        client.ebay.key_word.insert_one(page_dict)##save the html url in the dic
    client.close()



# csv_to_db()
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
from collections import Counter
import math

def make_product_name():
    file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/product_in_stock.csv'
    df = pd.read_csv(file_location)
    df = df.replace(np.nan, '', regex=True)
    Old_Product_Service_Name=df["Old_Product_Service_Name"].tolist()
    name=df["name"].tolist()
    make=df["make"].tolist()
    celica=df["celica"].tolist()
    liter = df["liter"].tolist()
    engine_code = df["engine_code"].tolist()
    engine_type_2 = df["engine_type_2"].tolist()
    value_number = df["value_number"].tolist()
    clyinder = df["clyinder"].tolist()
    car_year_model = df["car_year_model"].tolist()
    size=df["size"].tolist()
    result=[]

    count=0
    for i in range(len(name)):
        # if celica[i] :
        #     product_name=name[i]+ " "+ size[i]+" for "+make[i]+" "+celica[i]
        #
        #     print(product_name)
        #     print(len(product_name))
        #     if len(product_name)>80:
        #         count+=1
        #     print(count)
        #     print('')
        # else:
        if len(car_year_model[i])<20:
            product_name = name[i]+ " "+size[i]+" for " +make[i]+ " "+liter[i]+" "+engine_code[i]+" "+engine_type_2[i]+" "+value_number[i]+" "+car_year_model[i]
        else:
            product_name=name[i]+ " "+size[i]+" for " +make[i]+ " "+liter[i]+" "+engine_code[i]+" "+engine_type_2[i]+" "+value_number[i]

        print(product_name)
        print(len(product_name))
        if len(product_name) > 80:
            count += 1
        print(count)
        print('')
        row_dict=dict()
        row_dict['Old_Product_Service_Name']=Old_Product_Service_Name[i]
        row_dict['prduct_name']=product_name
        result.append(row_dict)
    df = pd.DataFrame(result)
    df.to_csv( 'product_name.csv')
make_product_name()
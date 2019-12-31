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

def click_make(driver,make):
    driver.get('http://www.safetyautoparts.com/webcatalog/tradcatalog.html')
    frame=driver.find_element_by_name('menuFrame')
    driver.switch_to_frame(frame)
    driver.find_element_by_xpath("//option[text()='" + make + "']").click()

def click_engine(driver,enginecode):
    # frame = driver.find_element_by_name('menuFrame')
    # driver.switch_to_frame(frame)
    driver.find_element_by_xpath("//option[@value='" + enginecode + "']").click()

def save_html_source(carmake,enginecode,enginename,html):
    client = MongoClient('mongodb://localhost:27017')
    page_dict = dict()
    page_dict['car_make'] = carmake
    page_dict['engine_code'] = enginecode
    page_dict['engine_name'] = enginename
    page_dict['html'] = html

    client.safety.html_page.insert_one(page_dict)##save the html url in the dic
    client.close()

def read_csv():
    file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/jis_application_final.csv'
    df=pd.read_csv(file_location)
    # df.sort_values("maker", inplace = True)
    # df.drop_duplicates(subset='maker',
    #                      keep='first', inplace=True)
    # makelist=df['maker'].tolist()
    # makelist=['Toyota','Honda']
    makelist=['Isuzu', 'Mitsubishi',
              'Nissan', 'Subaru', 'Suzuki', 'Acura','Infiniti', 'Hyundai',
              'Kia', 'Lexus','Nissan Ind/UD Trucks', 'Isuzu Industrial','Daihatsu',  'Scion',
                'Mitsubishi Ind/Fuso','Chrysler Trucks', 'Daewoo',  'Ford Trucks',
               'Chrysler Cars',  'Mazda Industrial', 'Toyota Ind/Hino','Ford Cars', 'GM Industrial',  'Saab',
               'GM Cars', 'GM Trucks'
               ]

    # makelist = ['Toyota', 'Honda', 'Mazda', 'Isuzu', 'Mitsubishi',
    #             'Nissan', 'Subaru', 'Suzuki', 'Acura', 'Hyundai',
    #             'Kia', 'Smart', 'Nissan Ind/UD Trucks', 'Isuzu Industrial',
    #             'Jeep', 'Volvo', 'Mitsubishi Ind/Fuso',
    #             'Honda Hybrid', 'BMW Hybrid', 'Chrysler Hybrid',
    #             'Subaru Hybrid', 'BMW', 'Chrysler Trucks', 'Audi',
    #             'Daewoo', 'Porsche', 'Nissan Hybrid', 'Ford Trucks',
    #             'Jaguar', 'Chrysler Cars', 'Ford Hybrid', 'Ford Cars',
    #             'GM Industrial', 'Infiniti', 'Saab', 'Fiat', 'Lexus',
    #             'Toyota Hybrid', 'Volkswagen Hybrid', 'GM Cars', 'GM Trucks',
    #             'Land Rover', 'Mazda Industrial', 'Toyota Ind/Hino',
    #             'GM Hybrid', 'Mercedes Benz', 'Daihatsu', 'Volkswagen',
    #             'Mercedes Benz Hybrid', 'Scion', 'Hyundai Hybrid']

    return makelist,df
# makelist=read_csv()
# print(makelist)
# random.shuffle(makelist)
# print(len(makelist))

def filter_out_scrapied_engine(enginelist):#filter the engine
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.html_page.find({})
    searched_engine = [page_dict['engine_code'] for page_dict in result]


    not_searched_engine = []
    for engine in enginelist:
        if engine not in searched_engine:
            print(engine)
            not_searched_engine.append(engine)
        else:
            # print(engine)
            continue
    return not_searched_engine
# makelist,df=read_csv()
# engine_list = df.loc[df['maker'] == 'Mazda', 'engine_number'].tolist()
# engine_list[7]= 'NA'
# print(len(engine_list))
# print(engine_list)
# engine_list= ['1KC', '3KC', '4KC', '4KE', '2E', '13AC', '3AC', '3E', '3EE', '5EFE', '1NZFE', '2TC', '4AC', '4ALC', '4AGEC', '4AGE', '4AGELC', '4AGZE', '4AF', '4AFE-1', '4AFE-2', '3TC', '7AFE', '1ZZFE', '2ZZGE', '2ZRFE', '1CLC', '1CTLC', '3RC', '8RC', '18RC', '21R', '2CTLC', '2SELC', '1VZFE', '3YEC', '3SGELC', '3SGTE', '3SFE', '3SFE-RAV4', '1AZFE', '4UGSE', '5SFE', '1L', '20R', '4YEC', '2M', '22R-E', '22R', '22RE', '22RTEC', '2TZFE', '2TZFZE', '2RZFE', '2AZFE', '2L', '2LT', '2ARFE', '2VZFE', '4M', '4ME', '2TRFE', '3RZFE', '1ARFE', '5ME', '5MGE', '7MGE', '7MGTE', '3VZE', '3VZFE', '1MZFE', '2JZGE', '2JZGTE', '3MZFE', '5VZFE', '2GRFE', '2GRFKS', '1F', '3FE', '1GRFE', '2F', '1FZFE', '1URFE', '2UZFE', '3URFE']
# print(filter_out_scrapied_engine(engine_list))
# np.random.shuffle(engine_list)
def filter_out_scrapied_make(makelist,df):
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.html_page.find({})
    searched_make = [page_dict['car_make'] for page_dict in result]
    #searched_make does not change so result is used once not like result2 below
    # print(searched_make)
    # result2 = client.safety.html_page.find({})
    # searched_engine1 = [page_dict['engine_code'] for page_dict in result2]
    # print(searched_engine1)
    # result2 = client.safety.html_page.find({})
    not_searched_make = []
    # makelist=['Mitsubishi','Nissan']

    for make in makelist:
        # print(make)
        # count_from_db = client.safety.html_page.find({'car_make':make}).count()
        # print (count_from_db)
        result2 = client.safety.html_page.find({})
        # find() function return a cursor to the db so we need to activate every time make change
        searched_engine = [page_dict['engine_code'] for page_dict in result2 if page_dict['car_make']==make]
        # print(searched_engine)

        enginelist = df.loc[df['maker'] == make, 'engine_number'].tolist()

        # print(len(searched_engine))
        # print(len(enginelist))
        # print("")

        if make not in searched_make:
            # print(make)
            not_searched_make.append(make)
        elif len(searched_engine)!=len(enginelist):
            not_searched_make.append(make)
            # print(len(searched_engine))
            # print(len(enginelist))
        # else:
        #     # print(engine)
        #     continue
    return not_searched_make

# makelist, df = read_csv()
# print(filter_out_scrapied_make(makelist,df))

def get_engine_code_list(df,make):

    enginelist = df.loc[df['maker'] == make, 'engine_number'].tolist()
    return enginelist
# make='Toyota'
# makelist,df=read_csv()
# print(get_engine_code_list(df,make))


def frame_switch(driver,name):
  driver.switch_to.frame(driver.find_element_by_name(name))


def amount_of_download():
    file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/jis_application_final.csv'
    df = pd.read_csv(file_location)
    maker=df["maker"].tolist()
    return Counter(maker)
# print(amount_of_download())






class safetyspider(Spider):
    name = "safety"
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


        self.driver.get('http://www.safetyautoparts.com/webcatalog/tradcatalog.html')

        makelist, df = read_csv()
        makelist = filter_out_scrapied_make(makelist,df)
        # makelist=np.random.shuffle(makelist)
        print(makelist)
        for make in makelist:
            # self.driver.get('http://www.safetyautoparts.com/webcatalog/tradcatalog.html')
            sleep(randint(5, 10))
            click_make(self.driver,make)
            sleep(randint(5, 10))
            print('make:'+make)
            enginelist =get_engine_code_list(df,make)
            # enginelist[7]='NA'
            # print('enginelist:'+enginelist)
            enginelist = filter_out_scrapied_engine(enginelist)
            if enginelist is None:
                continue
            # print('filtered list:'+enginelist)
            np.random.shuffle(enginelist)
            # print('shuffled lsit:'+enginelist)

            # self.count= self.count + 1
            # print('total scrapied item:'+self.count)
            # if self.count > 3:
            #     raise scrapy.exceptions.CloseSpider('------end of scrapy')

            # if len(enginelist)==0:
            #     continue

            for engine in enginelist:
                # print(engine)
                click_engine(self.driver,engine)
                sleep(randint(5, 10))
                carmake=make
                enginecode=engine
                enginename=self.driver.find_element_by_xpath("//option[@value='" + engine + "']").text

                self.driver.switch_to.default_content()
                frame_switch(self.driver, 'resultsFrame')

                html=self.driver.page_source

                self.driver.switch_to.default_content()
                frame_switch(self.driver, 'menuFrame')

                save_html_source(carmake, enginecode, enginename, html)
                print("save success: "+enginecode)
                self.count = self.count + 1
                print('This run scrapied item:' + str(self.count))

                if self.count == 20:
                    sleep(randint(3600, 3700))
                elif self.count == 40:
                    sleep(randint(7200, 7300))
                elif self.count >= 50:
                    raise scrapy.exceptions.CloseSpider('------end of scrapy')
                sleep(randint(300,600))

        raise scrapy.exceptions.CloseSpider('------end of scrapy')


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

def click_kit(driver,kitcode):
    frame=driver.find_element_by_name('menuFrame')
    driver.switch_to_frame(frame)
    # driver.find_element_by_xpath("//option[text()='" + kit + "']").click()
    driver.find_element_by_xpath("//option[@value='" + kitcode + "']").click()

def click_kit_number(driver,kit_number):
    # frame = driver.find_element_by_name('menuFrame')
    # driver.switch_to_frame(frame)
    driver.find_element_by_xpath("//option[text()='" + kit_number + "']").click()

def save_html_source(kitcode, kit_number, html):
    client = MongoClient('mongodb://localhost:27017')
    page_dict = dict()
    page_dict['kitcode'] = kitcode
    page_dict['kit_number'] = kit_number
    page_dict['html'] = html
    page_dict['kit'] = '(SECK) Complete Engine Kit'
    # if kitcode=='PS':
    #     page_dict['kit']='(SPR) Piston w Rings Set'
    # elif kitcode=='SECK':
    #     page_dict['kit']='(SECK) Complete Engine Kit'
    # elif kitcode=='TK':
    #     page_dict['kit']='(TK) Timing Kit w o Gears'
    # elif kitcode=='SRK':
    #     page_dict['kit']='(SRK) Safety Rering Kit'
    # elif kitcode=='TCK':
    #     page_dict['kit']='(TCK) Complete Timing Kit w Gears'
    # elif kitcode=='SEK':
    #     page_dict['kit']='(SEK) Safety Engine Kit'
    # else:
    #     page_dict['kit']='(TTK) 3-Piece Timing Kit'

    client.safety.kit_page.insert_one(page_dict)##save the html url in the dic
    client.close()

def read_csv():
    file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/kit_number.csv'
    df=pd.read_csv(file_location)

    # kitlist=['(SPR) Piston w Rings Set', '(SECK) Complete Engine Kit', '(TK) Timing Kit w o Gears',
    #         '(SRK) Safety Rering Kit', '(TCK) Complete Timing Kit w Gears', '(SEK) Safety Engine Kit',
    #         '(TTK) 3-Piece Timing Kit']

    kitlist = ['(SECK) Complete Engine Kit']

    # kitcodelist=['PS', 'SECK', 'TK', 'SRK', 'TCK', 'SEK', 'TTK']

    kitcodelist = ['SECK']

    return kitlist,df,kitcodelist


def filter_out_scrapied_kit_number(kit_number_list):#filter the engine
    client = MongoClient('mongodb://localhost:27017')
    result = client.safety.kit_page.find({})
    searched_kit_number = [page_dict['kit_number'] for page_dict in result]

    not_searched_kit_number = []
    for kit_number in kit_number_list:
        if kit_number not in searched_kit_number:
            not_searched_kit_number.append(kit_number)
        else:
            print(kit_number)
            continue
    return not_searched_kit_number



def get_kit_number_list(df,kitcode):

    kit_number_list = df.loc[df['kitcode'] == kitcode, 'kit_number'].tolist()
    return kit_number_list
# kitcode='PS'
# kitlist,df,kitcodelist=read_csv()
# print(get_kit_number_list(df,kitcode))



def frame_switch(driver,name):
  driver.switch_to.frame(driver.find_element_by_name(name))



class safetyspider(Spider):
    name = "safetykit"
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

        kitlist, df, kitcodelist = read_csv()
        for kitcode in kitcodelist:
            sleep(randint(5, 10))
            click_kit(self.driver,kitcode)
            sleep(randint(5, 10))
            print('kitcode:'+kitcode)
            kit_number_list =get_kit_number_list(df,kitcode)

            kit_number_list = filter_out_scrapied_kit_number(kit_number_list)

            np.random.shuffle(kit_number_list)


            if len(kit_number_list)==0:
                continue

            for kit_number in kit_number_list:
                click_kit_number(self.driver,kit_number)
                sleep(randint(5, 10))
                kitcode=kitcode
                kit_number=kit_number


                self.driver.switch_to.default_content()
                frame_switch(self.driver, 'resultsFrame')

                html=self.driver.page_source

                self.driver.switch_to.default_content()
                frame_switch(self.driver, 'menuFrame')

                save_html_source(kitcode, kit_number, html)
                print("save success: "+kit_number)
                self.count = self.count + 1
                print('this run scrapied item:' + str(self.count))

                # if self.count == 10:
                #     sleep(randint(3600, 3700))
                # elif self.count == 20:
                #     sleep(randint(7200, 7300))
                # elif self.count >= 30:
                #     raise scrapy.exceptions.CloseSpider('------end of scrapy')
                # sleep(randint(300,600))



                if self.count >= 30:
                    raise scrapy.exceptions.CloseSpider('------end of scrapy')
                sleep(randint(300,600))

        raise scrapy.exceptions.CloseSpider('------end of scrapy')


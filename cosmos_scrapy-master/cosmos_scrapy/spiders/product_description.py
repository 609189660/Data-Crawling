from scrapy.selector import Selector
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint

def get_html():
    filename = 'engine_part_description.html'
    f = open(filename, "r").read()
    return f

def read_from_csv():
    file_location = 'C:/Users/Server/PycharmProjects/cosmos_scrapy/cosmos_scrapy/spiders/product_in_stock.csv'
    df = pd.read_csv(file_location)
    df = df.replace(np.nan, '', regex=True)
    Old_Product_Service_Name = df["Old_Product_Service_Name"].tolist()
    name = df["name"].tolist()
    make = df["make"].tolist()
    # celica = df["celica"].tolist()
    liter = df["liter"].tolist()
    engine_code = df["engine_code"].tolist()
    engine_type_2 = df["engine_type_2"].tolist()
    value_number = df["value_number"].tolist()
    clyinder = df["clyinder"].tolist()
    car_year_model = df["car_year_model"].tolist()
    # size = df["size"].tolist()
    return make,car_year_model,name,Old_Product_Service_Name,engine_code,liter,engine_type_2,value_number,clyinder

def make_new_description(html,make,car_year_model,name,Old_Product_Service_Name,engine_code,liter,engine_type_2,value_number,clyinder):

    result=[]
    for i in range(len(make)):
        markup = html
        soup = BeautifulSoup(markup, features="lxml")
        carmake = soup.findAll("span", {"id": "make"})
        carmodel = soup.findAll("span", {"id": "model"})
        component = soup.findAll("span", {"id": "component"})
        jispartnum = soup.findAll("span", {"id": "jispartnum"})
        enginecode = soup.findAll("span", {"id": "engine_code"})
        liters = soup.findAll("span", {"id": "liter"})

        for j in carmake:
            j.string = make[i]
        for j in carmodel:
            j.string = car_year_model[i]
        for j in component:
            j.string = name[i]
        for j in jispartnum:
            j.string = Old_Product_Service_Name[i]
        for j in enginecode:
            j.string = engine_code[i]
        for j in liters:
            j.string= liter[i]+', '+engine_type_2[i]+', '+value_number[i]+', '+clyinder[i]
        result.append(soup)
        print(i)

    return result


html=get_html()
make,car_year_model,name,Old_Product_Service_Name,engine_code,liter,engine_type_2,value_number,clyinder=read_from_csv()
result=make_new_description(html,make,car_year_model,name,Old_Product_Service_Name,engine_code,liter,engine_type_2,value_number,clyinder)
result_list = []
for i in range(len(make)):
    soup=result[i]
    row_dict = dict()
    row_dict['description']=str(soup)
    row_dict['sku']=Old_Product_Service_Name[i]
    result_list.append(row_dict)
    # print(str(soup))
df = pd.DataFrame(result_list)
df.to_csv('test.csv')

    # Html_file= open("description-"+str(i)+".html","w")
    # Html_file.write(str(soup))
    # Html_file.close()

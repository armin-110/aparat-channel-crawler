print('بسمه الله الرحمن الرحیم')
print('salam bar mohammadreza dehghan amiri')
# from tkinter import S
import datetime
from httpx import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as b
import pandas as pd
import numpy as np
from bs2json import bs2json
import re
import requests
import time
import requests
import copy
import itertools
from copy import deepcopy
# import similarity_detection
# import lenz_preprocessing
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor
from iteration_utilities import unique_everseen
#step3: 
import psycopg2
import pandas.io.sql as psql
from sqlalchemy import create_engine


connection = psycopg2.connect(user="postgres",
                                password="12344321",
                                host="10.32.141.17",
                                port="5432",
                                database="Armin01")
cursor = connection.cursor()

df0= psql.read_sql("SELECT * FROM public.aparat_metatest1", connection)
print(len(df0))
channel_link= list(itertools.chain(*df0.iloc[:, [3]].values.tolist()))
print(len(channel_link))
channel_link_uniq = list(dict.fromkeys(channel_link))
print(len(channel_link_uniq))
# print(len(list(unique_everseen(channel_link))))
# content_link = list(itertools.chain(*df0.iloc[:, [8]].values.tolist()))
# content_link_uniq = list(dict.fromkeys(content_link))
# print(len(content_link_uniq))

import aparat_channel_meta

def get_metadata(channel_link):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    gf = aparat_channel_meta.GETMETA(channel_link,driver)
    gf.get_meta()
    driver.close()
    return (aparat_channel_meta.out_meta_list[0])


engine = create_engine('postgresql://postgres:12344321@10.32.141.17/aparat_channel',pool_size=20, max_overflow=100,)
con=engine.connect()

for i in range(len(channel_link_uniq)):
    print(channel_link_uniq[i])
    meta=get_metadata(channel_link_uniq[i])
    if (meta['views']=='0')and(meta['video number']=='0'):
        meta=get_metadata(channel_link_uniq[i])
    print(meta)
    date_i=datetime.datetime.now()
    meta['crawling_date']=str(date_i.date()).replace('-','')+str(date_i.time()).split(':')[0]
    data_frame =pd.DataFrame(meta,index=[0])
    data_frame.to_sql('aparat_channel_meta',con,if_exists='append', index=False)
    
# meta=get_metadata('https://www.aparat.com/u_11513129')
# print(meta)

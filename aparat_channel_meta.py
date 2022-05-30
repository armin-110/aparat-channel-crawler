from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import pandas as pd
import numpy as np
from bs2json import bs2json
import re
import json
import copy
from copy import deepcopy
import requests
from collections import OrderedDict
from iteration_utilities import unique_everseen
import time
import itertools
import pyodbc 
from pyodbc import *

converter = bs2json()

out_meta_list=[]
###############################
class GETMETA():
    def __init__ (self,channel_link,driver):
        self.channel_link = channel_link
        self.driver = driver
        ##################################################################################

    def get_meta(self):
        meta_dic = {'channel_link':self.channel_link, 'views':'0','video number':'0','facebook_link':'','telegram_link':'','twitter_link':'','instagram_link':'','site_link':'','channel_publish_time':''}

        try:
            out_meta_list.clear()
            # time.sleep(3) 
            print(self.channel_link)
            self.driver.get(self.channel_link)
            # self.driver.refresh()
            # uid = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.tab-item:nth-child(4) > a:nth-child(1) > button:nth-child(1)')))
            # uid.send_keys(Keys.ENTER)
            try:
                uid = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.tab-item:nth-child(4) > a:nth-child(1) > button:nth-child(1)')))
                uid.send_keys(Keys.ENTER)
            except:
                try:
                    self.driver.refresh()
                    uid = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#listWrapperundefined > div > div.sc-jlRLRk.dSxuoR > ul > div > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > li:nth-child(5) > a > button')))
                    uid.send_keys(Keys.ENTER)
                except:
                    self.driver.refresh()
                    uid = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#listWrapperundefined > div > div.sc-jlRLRk.eLJBp > ul > div > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > li:nth-child(4) > a > button')))
                    uid.send_keys(Keys.ENTER)

            try:
                fb= WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#listWrapperundefined > div > div.sc-jlRLRk.eLJBp > div')))
            except:
                try:
                    fb= WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-kTLmzF > div:nth-child(1) > div:nth-child(1)')))
                except:
                    fb= WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fmciRz > div:nth-child(1) > div:nth-child(1)')))
            html=self.driver.execute_script("return arguments[0].outerHTML;",fb)
            page_html_soup=b(html,'html.parser')
            # print(page_html_soup)

            class_find=page_html_soup.findAll('span',{'class':'about-channel__total-videos item-info'})
            converter = bs2json()
            json_class_find = converter.convertAll(class_find)  
            # print(json_class_find[0]['text'])#video number
            pattern = '[:ا-ی]'
            if 'هزار' in json_class_find[0]['text']:
                meta_dic['video number']= float(re.sub(pattern,'', json_class_find[0]['text']))*10000
            elif 'میلیون' in json_class_find[0]['text']:
                meta_dic['video number']=float(re.sub(pattern,'', json_class_find[0]['text']))*10000000
            else:
                meta_dic['video number']=float(re.sub(pattern,'', json_class_find[0]['text']))    
            
            ########################################################################################
            class_find=page_html_soup.findAll('span',{'class':'about-channel__total-view item-info'})
            converter = bs2json()
            json_class_find = converter.convertAll(class_find)  
            # print(json_class_find[0]['text'])#views
            pattern = '[:ا-ی]'
            if 'هزار' in json_class_find[0]['text']:
                meta_dic['views']=int(float(re.sub(pattern,'', json_class_find[0]['text']))*1000)
            elif 'میلیون' in json_class_find[0]['text']:
                meta_dic['views']=int(float(re.sub(pattern,'', json_class_find[0]['text']))*1000000)
            else:
                meta_dic['views']=int(float(re.sub(pattern,'', json_class_find[0]['text'])))

            #########################################################################################
            class_find=page_html_soup.findAll('span',{'class':'about-channel__start-date item-info'})
            converter = bs2json()
            json_class_find = converter.convertAll(class_find)  
            # print(json_class_find[0]['text'])#views
            meta_dic['channel_publish_time']=json_class_find[0]['text']
            
            #########################################################################################
            try:
                class_find=page_html_soup.findAll('ul',{'class':'list-socials'})
                converter = bs2json()
                json_class_find = converter.convertAll(class_find)  
                # print(json_class_find)
                for i in range(len(json_class_find[0]['li'])):
                    # print(json_class_find[0]['li'][i]['a']['attributes']['href'])
                    if 'facebook' in json_class_find[0]['li'][i]['a']['attributes']['href']:
                        meta_dic['facebook_link']=json_class_find[0]['li'][i]['a']['attributes']['href']
                
                    if 'telegram' in json_class_find[0]['li'][i]['a']['attributes']['href']:
                        meta_dic['telegram_link']=json_class_find[0]['li'][i]['a']['attributes']['href']

                    if 'twitter' in json_class_find[0]['li'][i]['a']['attributes']['href']:
                        meta_dic['twitter_link']=json_class_find[0]['li'][i]['a']['attributes']['href']
                
                    if 'instagram' in json_class_find[0]['li'][i]['a']['attributes']['href']:
                        meta_dic['instagram_link']=json_class_find[0]['li'][i]['a']['attributes']['href']

                    if 'ir' in json_class_find[0]['li'][i]['a']['attributes']['href']:
                        meta_dic['site_link']=json_class_find[0]['li'][i]['a']['attributes']['href']
            except:
                pass
            # print(meta_dic)
            out_meta_list.append(meta_dic)

        except:
            out_meta_list.append(meta_dic)

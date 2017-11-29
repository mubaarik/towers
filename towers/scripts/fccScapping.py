from file_processers import *
from polygon import *
from webscraper import *

import dropbox
import os

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 
import time
'''
Encloses a set of methods to download tower data of a given company from the FCC data
'''
class ReadFCC:
    def __init__(self,company = "AT&T",driver=None,token=None, output = None):
        self.token = token
        self.dpbx = dropbox.Dropbox(self.token)
        self.company = company
        self.output = output
        self.url = "http://wireless2.fcc.gov/UlsApp/AsrSearch/asrRegistrationSearch.jsp"
        self.select_xpath = '/html/body/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/form/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/select'
        self.text_box_xpath = '/html/body/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/form/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/input[1]'
        self.submit_btn_xpath = '/html/body/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/form/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/input[2]'
        self.driver = driver;#pointToAddrBrowse(browse(), url = self.url)
        self.table_xpath = '/html/body/table[4]/tbody/tr/td[2]/div/form/table[2]/tbody/tr/td'
        self.next_xpath = '//a[@title="Next page of results"]'
    def driverUpdate(self):
        self.driver.get(self.url)
        print "driver: ", self.driver
    def byownerSearch(self):
        select = Select(self.driver.find_element_by_xpath(self.select_xpath))
        select.select_by_visible_text("By Owner Name")
        box = self.driver.find_element_by_xpath(self.text_box_xpath).send_keys(self.company)
        submit_btn = self.driver.find_element_by_xpath(self.submit_btn_xpath).click()
        return self.driver
    def search_area(self,lat = (41,41,7),longi=(70,31,8), rad = 40):
        lat_deg = self.driver.find_element_by_name('fiLatDeg').send_keys(lat[0])
        lat_min = self.driver.find_element_by_name('fiLatMin').send_keys(lat[1])
        lat_sec = self.driver.find_element_by_name('fiLatSec').send_keys(lat[2])
        lon_deg = self.driver.find_element_by_name('fiLongDeg').send_keys(longi[0])
        lon_min = self.driver.find_element_by_name('fiLongMin').send_keys(longi[1])
        lon_sec = self.driver.find_element_by_name('fiLongSec').send_keys(longi[2])
        rad = self.driver.find_element_by_name('fiRadius').send_keys(rad)
        
        submit= "/html/body/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td[3]/form/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input[1]"
        self.driver.find_element_by_xpath(submit).click()
        return self.driver
        
        
    def change_columns(self,df):
        _df = df[df.index>0]
        colmns = df[df.index==0].values
        _df = _df.rename(columns = {name:colmns[0][int(name)] for name in _df.columns})
        return _df
    def extract_table(self):
        try:
            table = self.driver.find_element_by_xpath(self.table_xpath)
            html = table.get_attribute('innerHTML')
            df = pd.read_html(html)
            #print "dataframe?: ", df
            if len(df)>2:
                df = df[2]
                dataframe = self.change_columns(df)
                if isinstance(self.output, pd.DataFrame):
                    self.output = pd.concat([self.output,dataframe])
                else:
                    self.output = dataframe
        except NoSuchElementException:
            print "No Towers for: "+str(self.company)
        except IndexError:
            print "No Towers for: "+str(self.company)
    def extract_records(self):
        while True:
            time.sleep(5)
            self.extract_table()
            try:
                self.driver.find_element_by_xpath(self.next_xpath).click()
            except NoSuchElementException:
                break
    def write_to_csv(self, drpbx_upload=False):
        self.driverUpdate()
        time.sleep(2)
        self.byownerSearch()
        time.sleep(2)
        self.extract_records()
        if self.output is not None:
            data_file = 'csv_files/'+self.company+'.csv'
            self.output.to_csv(data_file)
            if drpbx_upload:
                f = open(data_file,'rb')
                data = f.read()
                f.close()
                path = '/'+data_file
                self.dpbx.files_upload(data,path,dropbox.files.WriteMode.add)
                os.remove(data_file)
    def click_and_write(self,name,drpbx_upload=False):
        self.driverUpdate()
        time.sleep(2)
        self.search_area()
        #self.driver = self.driver.get(url)
        time.sleep(2)
        self.extract_records()
        if self.output is not None:
            data_file = 'csv_files/'+name+'.csv'
            self.output.to_csv(data_file)
            #self.extract_records()
            if drpbx_upload:
                f = open(data_file,'rb')
                data = f.read()
                f.close()
                path = '/'+data_file
                self.dpbx.files_upload(data,path,dropbox.files.WriteMode.add)
                os.remove(data_file)
        
                

def changeColumns(dataframe):
    data = dataframe[dataframe.index>0]
    cols = dataframe[dataframe.index==0].values
    columns = {name:cols[0][int(name)] for name in data.columns}
    frame = data.rename(columns = {name:cols[0][int(name)] for name in data.columns})
    return frame
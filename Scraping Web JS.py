from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

driver = webdriver.Chrome('D:/Aplikasi/chromedriver.exe')
driver.get('https://www.jobstreet.co.id/')
time.sleep(3)

kotak_input = driver.find_element_by_xpath('//*[@id="locationAutoSuggest"]')
kotak_input.send_keys('semarang')

search = driver.find_element_by_xpath('//*[@id="contentContainer"]/div/div[1]/div/div/div/div/div[2]/div/form/div/div/div[2]/div[4]/button').click()
time.sleep(3)

data = pd.DataFrame({'Link':[],
                     'Posisi':[], 
                     'Perusahaan':[], 
                     'Kota':[], 
                     'Gaji':[], 
                     'Tanggal':[]})

bs = BeautifulSoup(driver.page_source, 'lxml') 
postings = bs.find_all('div', class_='sx2jih0 zcydq876 zcydq866 zcydq896 zcydq886 zcydq8n zcydq856 zcydq8f6 zcydq8eu')


i = 0
while True:
    bs = BeautifulSoup(driver.page_source, 'lxml') 
    postings = bs.find_all('div', class_='sx2jih0 zcydq876 zcydq866 zcydq896 zcydq886 zcydq8n zcydq856 zcydq8f6 zcydq8eu')
    i = i + 1
    for post in postings:
        link= post.find('a', class_='_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h').get('href')
        full_link = 'https://www.jobstreet.co.id/' + link
        posisi = post.find('span', class_= 'sx2jih0').text
        perusahaan = post.find('span', class_= 'sx2jih0 zcydq84u zcydq80 iwjz4h0').text
        kota = post.find('span', class_= 'sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvc7').text
        tanggal = post.find('span', class_= 'sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1y _18qlyvc1 _18qlyvc7').text
        try:
            gaji = post.find_all('span', class_= 'sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvc7')[1].text
        except:
            gaji = 'N/A'
            
        data = data.append({'Link':full_link,
                             'Posisi':posisi, 
                             'Perusahaan':perusahaan, 
                             'Kota':kota, 
                             'Gaji':gaji, 
                             'Tanggal':tanggal}, ignore_index = True)
        
    if i == 1:
        try:
            lanjut = bs.find('a', class_= 'sx2jih0 zcydq896 zcydq886 zcydq8o zcydq856 zcydq8ea zcydq8h zcydq8y zcydq8x IQYn5_0 _18qlyvc14 _18qlyvc17 zcydq832 zcydq835').get('href')
            driver.get('https://www.jobstreet.co.id/' + lanjut)
        except:
            break
    else: 
        try:
            lanjut = bs.find_all('a', class_= 'sx2jih0 zcydq896 zcydq886 zcydq8o zcydq856 zcydq8ea zcydq8h zcydq8y zcydq8x IQYn5_0 _18qlyvc14 _18qlyvc17 zcydq832 zcydq835')[1].get('href')
            driver.get('https://www.jobstreet.co.id/' + lanjut)
        except:
            break
        

data.to_csv('Loker Semarang.csv')

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

#laman web yang akan jadi target scraping
url = ('https://www.jobstreet.co.id/')

#melihat response dari server web yang akan discraping
test = requests.get(url)

# Lokasi tempat penyimpanan lokal aplikasi chromedriver
driver = webdriver.Chrome('D:/Aplikasi/chromedriver.exe')
driver.get(url)

#time sleep dapat diubah sesuai dengan kecepatan internet. 
time.sleep(1)

#memasukkan kata yang akan dicari pada pencarian kota / kabupaten
kotak_input = driver.find_element_by_xpath('//*[@id="locationAutoSuggest"]')
kotak_input.send_keys('semarang')

#memasukkan kata yang akan dicari pada pencarian pekerjaan apa yang ingin dicari
name_job = driver.find_element_by_xpath('//*[@id="searchKeywordsField"]')
name_job.send_keys ('data scientist')

#otomatis melakukan pencarian setelah memasukkan kata kunci dikolom pencarian
search = driver.find_element_by_xpath('//*[@id="contentContainer"]/div/div[1]/div/div/div/div/div[2]/div/form/div/div/div[2]/div[4]/button').click()
time.sleep(1)

#opsi selain menggunakan click pada kolom pencarian. Gunakan salah satu agar proses scraping dapat berjalan. 
kotak_input.send_keys(Keys.ENTER)

# Membuat Dataframe kosong untuk nanti dimasukkan data dari web ke dalam dataframe
data = pd.DataFrame({'Link':[],
                     'Posisi':[], 
                     'Perusahaan':[], 
                     'Kota':[], 
                     'Gaji':[], 
                     'Tanggal':[]})
'''
# Mengambil informasi dengan format html di python
bs = BeautifulSoup(driver.page_source, 'lxml') 

#jika pada halaman awal scraping akan lanjut scraping pada halaman berikutnya sampai semua data didapatkan
postings = bs.find_all('div', class_='sx2jih0 zcydq876 zcydq866 zcydq896 zcydq886 zcydq8n zcydq856 zcydq8f6 zcydq8eu')
'''

i = 0
while True:
    bs = BeautifulSoup(driver.page_source, 'lxml') 
    postings = bs.find_all('div', class_='sx2jih0 zcydq876 zcydq866 zcydq896 zcydq886 zcydq8n zcydq856 zcydq8f6 zcydq8eu')
    i = i + 1
    for post in postings:
        link= post.find('a', class_='_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h').get('href')
        full_link = url + link
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
                             'Tanggal':tanggal}, 
                           ignore_index = True)
        
    if i == 1:
        try:
            lanjut = bs.find('a', class_= 'sx2jih0 zcydq896 zcydq886 zcydq8o zcydq856 zcydq8ea zcydq8h zcydq8y zcydq8x IQYn5_0 _18qlyvc14 _18qlyvc17 zcydq832 zcydq835').get('href')
            driver.get(url + lanjut)
        except:
            break
    else: 
        try:
            lanjut = bs.find_all('a', class_= 'sx2jih0 zcydq896 zcydq886 zcydq8o zcydq856 zcydq8ea zcydq8h zcydq8y zcydq8x IQYn5_0 _18qlyvc14 _18qlyvc17 zcydq832 zcydq835')[1].get('href')
            driver.get(url + lanjut)
        except:
            break
        
# Mengeksport hasil dataframe yang telah discraping dalam format .csv dan dapat di sort berdasarkan kebutuhan
data.to_csv('Loker Semarang.csv')


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bts4
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import re
#Set the browser settings and return the profile
def browserProfile():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', '~/Downloads/towers')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    
    return profile


#open the firefox session
def browse(profile = None):
    driver = None;
    if profile != None:
        driver = webdriver.Firefox(firefox_profile=profile)
    else:
        driver = webdriver.Firefox()
    return driver

#filing the Antenna Search address form
def fill_form(driver, address,city, state, zipCode, url=None):
    if url == None:
        url = "http://www.antennasearch.com"
    driver.get(url)
    form  = driver.find_element_by_xpath("//form[@Action='sitestart.asp']")
    addr = driver.find_element_by_name('AddressIn').send_keys(address)
    town = driver.find_element_by_name('CityName').send_keys(city)
    providence = driver.find_element_by_name('StateName').send_keys(state)
    post_code = driver.find_element_by_name('ZipCodeNum').send_keys(zipCode)
    form.submit()
    return driver

#input src="/images/process.png"
def process(driver):
    xpath2 = '//input[@name="raditem"]'
    print "processing.................."
    try:
        #print "element: "+driver.page_source#+driver.find_element_by_xpath(xpath2)
        WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, xpath2))).click()
    except Exception as e:
        print e.message 
    xpath = '//input[@src="/images/process.png"]'
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, xpath))).click()

    return driver
def download(driv, address = "129 Franklin Street",city = 'Cambridge', state='MA', zipCode='02139'):
    driver = fill_form(driv,address,city, state, zipCode)
    default=driver = process(driver)
    link_text = 'Downloads Records'
    driver.implicitly_wait(200)
    #element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, link_text)))
    #element.click()
    driver.find_element_by_link_text('Download Records').click()
    return driver


#converting from latitudal points to address 
def pointToAddrBrowse(driv, url = None):
    if url==None:
        url = 'https://www.findlatitudeandlongitude.com/find-address-from-latitude-and-longitude'
    driv.get(url)
    return driv
    
def fillLocation(drv, lat, longi):
    #driv = 
    #location_form = drv.find_element_by_xpath("//form[@name='load_location']")
    lat_slot = drv.find_element_by_xpath("//input[@name='lat']").send_keys(str(lat))
    long_slot = drv.find_element_by_xpath("//input[@name='lon']").send_keys(str(longi))
    load_but = drv.find_element_by_xpath("//input[@name = 'load_latlon_button']").click()
    return drv
def cleanParts(addr):
    addr_parts = addr.split(',')
    print "address: "+str(addr_parts)
    #55 Tom Nevers Rd, Nantucket, MA 02554, USA
    _addr = []
    for part in addr_parts:
        part = part.strip()
        if len(part)>=2:
            _addr.append(part)
    assert(len(_addr)==4), 'expected: st.,city, state zip, country. found: '+str(_addr)
    print _addr

    zipcode = max(re.findall('[0-9]+', _addr[2]), key = len)
    state = max(_addr[2].split(zipcode), key = len).strip()
    street = _addr[0]
    city = _addr[1]
    country = _addr[-1]
    return street,city, state, zipcode,country



def extract_address(driv, lat = 42.948057, longi = -70.589209):
    driv = pointToAddrBrowse(driv)
    drv = fillLocation(driv, lat, longi)
    driv.implicitly_wait(10)
    time.sleep(3)
    mybs4 = bts4(drv.page_source, 'html.parser')
    addr_span = mybs4.find_all('span', id='address')[0]
    addr_span = bts4(str(addr_span))
    print "addr_span: "+str(addr_span)
    addr_breakdown = bts4(str(addr_span.find_all(attrs={'class':'value'})[0])).get_text()
    
    return cleanParts(addr_breakdown)




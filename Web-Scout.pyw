import os
import urllib.request
import bs4 as bs
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from twilio.rest import Client

"""
- Check Amazon and Powerblock using Chromedriver
- Check RepFitness using urllib
- Will send text message to phone number stored in environment variable
"""

#=================================
# Setup
#=================================

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
my_number = os.environ['Phone_Number']
twilio_number = os.environ['TWILIO_NUMBER']

client = Client(account_sid, auth_token)

# get the path of ChromeDriverServer
dir = os.path.dirname(__file__)
chrome_driver_path = dir + "\chromedriver.exe"

# make the browser window invisible
options = Options()
options.headless = True

# create a new Chrome session
driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

# Let the driver try to find the content for 10 seconds
driver.implicitly_wait(10)

# get the absolute path, since we'll be running this from command line
dirname = os.path.dirname(__file__)

# build log file paths
log = os.path.join(dirname, 'Web-Scout.log')
log2 = os.path.join(dirname, 'Availability.log')

# Open log file
f = open(log, "a")
f2 = open(log2, "a")

#=================================
# Functions
#=================================

# send specified text using twilio
def send_message(message_body):
    message = client.messages.create(body=message_body, from_='+18184505165', to=my_number)

#====================================
# Powerblock Compact Stand (Amazon)
#====================================

# create a new Chrome session
driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

# Let the driver try to find the content for 10 seconds
driver.implicitly_wait(10)

# powerblock amazon url 
url='https://www.amazon.com/POWERBLOCK-Compact-Weight-Stand-Black/dp/B01A9981M0/ref=sr_1_1?crid=1F57GF306BHXP&dchild=1&keywords=powerblock+compact+weight+stand&qid=1597100715&sprefix=powerblock+com%2Caps%2C203&sr=8-1'

# test url
url2 = 'https://www.amazon.com/Ghost-Tsushima-PlayStation-4/dp/B08BSKT43L/ref=zg_bsnr_videogames_home_1?_encoding=UTF8&psc=1&refRID=1Y7M1E00G5NXSZJ0X6R4'

# get the page text
driver.get(url)
html = driver.page_source
soup = bs.BeautifulSoup(html, 'lxml')
amz_price = soup.find(id='priceblock_ourprice')

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# if price tag has a value send the notification
if not amz_price:
    print('Powerblock Large Compact Stand is not available on Amazon {}'.format(dt_string))
else:
    body = 'Powerblock Large Compact Stand is available {} MT \n {}'.format(dt_string, url)
    send_message(body)
    print(body)
    f2.write(body)    
 
# close the browser window
driver.quit()

#========================================
# Powerblock Compact Stand (Powerblock)
#========================================

# create a new Chrome session
driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

# Let the driver try to find the content for 10 seconds
driver.implicitly_wait(10)

# powerblock url 
url='https://powerblock.com/product/compact-stand/'

# get the page text
driver.get(url)

select = Select(driver.find_element_by_id('pa_size'))
select.select_by_visible_text('Large')

html = driver.page_source
soup = bs.BeautifulSoup(html, 'lxml')
check = soup.findAll("p", {"class": "stock out-of-stock"})

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

if len(check) > 0:
    print('Powerblock Large Compact Stand is not available on PB {}'.format(dt_string))
else:
    body = 'Powerblock Large Compact Stand is available {} MT \n {}'.format(dt_string, url)
    send_message(body)
    print(body)
    f2.write(body)

#========================================
# pro-exp-stage-3-kit-70-90 (Powerblock)
#========================================

# create a new Chrome session
driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

# Let the driver try to find the content for 10 seconds
driver.implicitly_wait(10)


url='https://powerblock.com/product/pro-exp-stage-3-kit-70-90/'


# get the page text
driver.get(url)

html = driver.page_source
soup = bs.BeautifulSoup(html, 'lxml')
check = soup.findAll("p", {"class": "stock out-of-stock"})

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

if len(check) > 0:
    print('Pro-exp-stage-3-kit-70-90 is not available {}'.format(dt_string))
else:
    body = 'Pro-exp-stage-3-kit-70-90 is available {} MT \n {}'.format(dt_string, url)
    send_message(body)
    print(body)
    f2.write(body)

#===========================================
# Pro-series-kettlebell-handle(Powerblock)
#===========================================

url = 'https://powerblock.com/product/pro-series-kettlebell-handle/'

# get the page text
driver.get(url)

html = driver.page_source
soup = bs.BeautifulSoup(html, 'lxml')
check = soup.findAll("p", {"class": "stock out-of-stock"})

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

if len(check) > 0:
    print('Pro-series-kettlebell-handle is not available {}'.format(dt_string))
else:
    body = 'Pro-series-kettlebell-handle is available {} MT \n {}'.format(dt_string, url)
    send_message(body)
    print(body)
    f2.write(body)

#=====================
# REP AB 3000
#=====================

# open the url
url = 'https://www.repfitness.com/strength-equipment/strength-training/benches/rep-ab3000-fid-adj-bench'
source = urllib.request.urlopen(url).read()

#get the soup
soup = bs.BeautifulSoup(source,'lxml')
availability = soup.findAll("p", class_="availability out-of-stock")

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# Check if availability tag object has length greater than 0
if len(availability) > 0:
    print('AB-3000 is not available {}'.format(dt_string)) 
    
else:
    # send alert
    body = 'AB-3000 is available {} MT'.format(dt_string)
    send_message(body)
    print(body)    
    f2.write(body)
    os.system("start \"\" {}".format(url))    

#=====================
# REP AB 3100
#=====================

# open the url
url = 'https://www.repfitness.com/strength-equipment/strength-training/benches/rep-ab-3100-fi-bench'
source = urllib.request.urlopen(url).read()

#get the soup
soup = bs.BeautifulSoup(source,'lxml')
availability = soup.findAll("p", class_="availability out-of-stock")

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# Check if availability tag object has length greater than 0
if len(availability) > 0:
    print('AB-3100 is not available {}'.format(dt_string)) 
    
else:
    # send alert
    body = 'AB-3100 is available {} MT'.format(dt_string)
    send_message(body)
    print(body)    
    f2.write(body) 


#=====================
# REP AB 5000
#=====================

# open the url
url = 'https://www.repfitness.com/strength-equipment/strength-training/benches/rep-ab-5000'
source = urllib.request.urlopen(url).read()

#get the soup
soup = bs.BeautifulSoup(source,'lxml')
availability = soup.findAll("p", class_="availability out-of-stock")

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# Check if availability tag object has length greater than 0
if len(availability) > 0:
    print('AB-5000 is not available {}'.format(dt_string))
    
else:
    # send alert
    body = 'AB-5000 is available {} MT'.format(dt_string)
    send_message(body)
    print(body)    
    f2.write(body)

    
#=====================
# REP AB 5100
#=====================

# open the url
url = 'https://www.repfitness.com/rep-ab-5100'
source = urllib.request.urlopen(url).read()

#get the soup
soup = bs.BeautifulSoup(source,'lxml')
availability = soup.findAll("p", class_="availability out-of-stock")

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# Check if availability tag object has length greater than 0
if len(availability) > 0:
    print('AB-5100 is not available {}'.format(dt_string))  
    
else:
    # send alert
    body = 'AB-5100 is available {}!'.format(dt_string)
    send_message(body)
    print(body)
    f2.write(body)

#=====================
# WRAP-UP
#=====================

# close the browser window
driver.quit()

# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# log completion
f.write("Run completed at {}\n".format(dt_string))
f.close()
f2.close()
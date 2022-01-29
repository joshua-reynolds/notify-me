from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import urllib.request
import bs4 as bs
import webbrowser
from twilio.rest import Client

"""
-script for testing sites
"""

#=================================
# Setup
#=================================

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
my_number = os.environ['Phone_Number']
twilio_number = os.environ['TWILIO_NUMBER']

client = Client(account_sid, auth_token)

# send specified text using twilio
def send_message(message_body):
    message = client.messages.create(body=message_body, from_='+18184505165', to=my_number)

  
# get current time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

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


#====================================
# MAIN
#====================================





## powerblock amazon url 
#url='https://powerblock.com/product/pro-exp-stage-3-kit-70-90/'

## test url
#url2 = 'https://powerblock.com/product/elite-stage-2-kit-50-70/'

url3 = 'https://powerblock.com/product/pro-series-kettlebell-handle/'

## get the page text
#driver.get(url)

#html = driver.page_source
#soup = bs.BeautifulSoup(html, 'lxml')
##print(soup.prettify())
#check = soup.findAll("p", {"class": "stock out-of-stock"})

#if len(check) > 0:
    #print('unavailable')
#else:
    #print('available')

# separator
print('-'*20)

# powerblock url 
url='https://powerblock.com/product/compact-stand/'

# get the page text
driver.get(url)

select = Select(driver.find_element_by_id('pa_size'))
select.select_by_visible_text('Large')

html = driver.page_source
soup = bs.BeautifulSoup(html, 'lxml')
#print(soup.prettify())
check = soup.findAll("p", {"class": "stock out-of-stock"})

if len(check) > 0:
    print('unavailable')
else:
    print('available')

## if price tag has a value send the notification
#if amz_price:
    #body = 'Product is available {} MT'.format(dt_string)
    #send_message(body)
    #print(body)
    #webbrowser.open(url)
#else:
    #print('Product is not available {}'.format(dt_string))
    
# close the browser window
driver.quit()


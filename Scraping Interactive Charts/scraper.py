from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import datetime as dt
import pandas as pd

# Opening the connection and grabbing the page
my_url = 'https://www.google.com/webhp?hl=en'
option = Options()
option.headless = False
driver = webdriver.Chrome(options=option)
driver.get(my_url)
driver.maximize_window()

# Instantiating the action object
action = webdriver.ActionChains(driver)

# Performing the search

search_bar = WebDriverWait(driver,
                          20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/form/div[2]/'
                                                                              'div[1]/div[1]/div/div[2]/input')))

search_button = WebDriverWait(driver,
                              20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/'
                                                                              'div[1]/div[3]/center/input[1]')))

search_bar.send_keys('dollar euro')
search_button.click()

# To change to the time range to years uncomment the code below
#years = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]'
#                                    '/div/div/div/div/div/div[2]/div/div[1]/div/div[4]/div/div')
#years.click()
sleep(2)

# Grabbing the element and its size and location
element = WebDriverWait(driver,
                              20).until(EC.presence_of_element_located((By.XPATH,
                                                                        '/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/'
                                                                        'div/div[2]/div[2]/div/div/div[1]/div/div/div/'
                                                                        'div/div/div[2]/div/div[2]/div/div')))
loc = element.location
size = element.size
print(loc)
print(size)

# Moving the cursor to the extreme right of the object
action.move_to_element_with_offset(element, 301, 0).perform()

# Getting the first date and value pair
date = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/'
                                    'div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/span[4]').text
value = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/'
                                     'div[1]/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/span[1]').text

# Setting up the dictionary and the limit and pace variables
time_serie = {}
time_serie[date] = value

print(date, value)

limit = dt.datetime.strptime('05/20', '%m/%d')
pace = -5

# Scraping the data
while True:
    action.move_by_offset(pace, 0).perform()
    date = driver.find_element_by_xpath(
        '/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/'
        'div/div[2]/div/div/div[1]/span[4]').text
    value = driver.find_element_by_xpath(
        '/html/body/div[5]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/'
        'div/div[2]/div/div/div[1]/span[1]').text

    print(date, value)

    if dt.datetime.strptime(date, '%a, %d %b') < limit:
        print(dt.datetime.strptime(date, '%a, %d %b'))
        break

    if date in time_serie:
        pass
    else:
        time_serie[date] = value

driver.quit()

# Creating a DataFrame and exporting the .csv file
df = pd.DataFrame.from_dict(time_serie, orient='index', columns=['values'])
df.to_csv('moedas_google.csv')

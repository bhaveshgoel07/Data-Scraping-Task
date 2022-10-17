from selenium import webdriver                              #import the webdriver
from selenium.webdriver.support.ui import Select                              #for selecting drop down menus
import time                              #for sleep function
import pandas as pd                              #for data manipulation
from twocaptcha import TwoCaptcha                                 #for OCR

solver = TwoCaptcha('Your_API_Key_Here')                              #initialize TwoCaptcha object for OCR    

path_to_chrome_driver = "C:/SeleniumDriver/chromedriver.exe"
driver = webdriver.Chrome(path_to_chrome_driver)

url = "https://isarita.igrmaharashtra.gov.in/MH_ESEARCHNEW/Esearch/propertydetails/"

driver.get(url)
driver.implicitly_wait(10)                                #To wait for elements of website to load

years = driver.find_element_by_id("year")       
years.send_keys(2022)

form = driver.find_element_by_class_name("form-group").click()          #to close the dropdown which opened from year textbox



districts = driver.find_element_by_id("district_id")
district = Select(districts)
district.select_by_index(25)                                  #selecting 25th index from district_id drop down

time.sleep(2)                                                            # to wait for website to finish loading

tehsils = driver.find_element_by_id("tehsil_id")
tehsil = Select(tehsils)
tehsil.select_by_value("1")                               #selecting 25th index from tehsil_id drop down

time.sleep(3)                                                            #to wait for website to finish loading

villages = driver.find_element_by_id("village_id")
village = Select(villages)
village.select_by_value("46323")                        # Selecting element with value 46323 from the dropdown menu

prop_num = driver.find_element_by_id("property_no")
prop_num.send_keys(10)                                  #Entering 10 in the textbox of property number

captcha_img = driver.find_element_by_id("captcha_image")    
captcha_img.screenshot("foo.png")               #taking screenshot of the captcha
result = solver.normal('foo.png')               #sending screenshot of captcha to TwoSolver api

captcha = driver.find_element_by_id("captcha").send_keys(result['code'].upper())        #entering result from api to the captcha textbox

button = driver.find_element_by_id("btnadd").click()

time.sleep(10)                                             #to wait for table to load completely

show_entries = driver.find_element_by_name("tableparty_length")
show_entry = Select(show_entries)
show_entry.select_by_index(4)                               #to show all entries at once in the page


page = driver.page_source                           #to load html code of the page  for data extraction

df = pd.read_html(page)                             #loading the table into pandas dataframe
df[0].drop(columns = 'IndexII').to_csv("file.csv")      #writing dataframe to csv file
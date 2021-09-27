from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('GOOGLE_SHEET_api.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Facebook comment").sheet1
sheet.clear()
row = ["Url", "profile pic", "profile link", "name", "comment","ref link"]
sheet.insert_row(row, 1)
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\wing\\profile");

driver = webdriver.Chrome(options=chrome_options)
#url = 'https://www.facebook.com/MIRROR.WeAre/posts/961470301098626'
url = input("Enter Facebook Post:")
driver.get(url)

def get_comment(element):
    global time
    data = []
    #driver.find_element_by_xpath("//span[contains(text(), 'View more comments')]").click()
    ul = element.find_elements_by_xpath(".//div[contains(@aria-label,'Comment by')]")
    for x in ul:
        row = []
        try:
            x.find_element_by_xpath(".//div[contains(text(), 'See More')]").click()
        except NoSuchElementException as e:
            print("")
        pic = '=IMAGE(\"{}\")'.format(x.find_element_by_tag_name("image").get_attribute('xlink:href')) # profile pic
        profile_link = x.find_element_by_xpath(".//a").get_attribute('href') # profile link
        name = x.find_elements_by_xpath(".//a")[1].text # author  name
        try:
            comment = x.find_element_by_xpath(".//span[attribute::*[contains(local-name(), 'lang')]]").text #comment
        except NoSuchElementException as e:
            comment = ""  
        href = x.find_elements_by_xpath(".//a")[-1].get_attribute('href') #author  link
        row = [url,pic, profile_link, name, comment,href]
        print(row)
        data.append(row)
    sheet.insert_rows(data,2, value_input_option='USER_ENTERED')
    #element.find_element_by_xpath(".//span[contains(text(), 'View more comments')]").click()
def view_more(element):
    while True:
        try:
            element.find_element_by_xpath(".//span[contains(text(), 'View more comments')]").click()
            print("More Comment Found")
            time.sleep(2)
        except NoSuchElementException as e:
            get_comment(element)
            break
    
time.sleep(2)
post = driver.find_element_by_xpath("//div[attribute::*[contains(local-name(), 'aria-posinset')]]")
view_more(post)
 #find the first post



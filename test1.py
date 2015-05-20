import requests 
import selenium
import requests 
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def find_nth(haystack, needle, n):                                   #method to find the index of nth occurrence of a substring needle in a string haystack
    start = haystack.find(needle)
    while start >= 0 and n > 1:
          start = haystack.find(needle, start+len(needle))
          n -= 1
    return start
url="http://test.healthqrs.com/api/procedures/available"
r = requests.get(url)                                                             #load the page into r
soup = BeautifulSoup(r.content)
texts = soup.findAll(text=True)[0]
text=texts.split('}')
npilist=[]
for field in text:                                                                #get procedre code in npilist 
     npi=field[45:50]
     if "." in npi:
         temp=field[45:]
         i=find_nth(temp, '"', 1)
         npi=temp[:i]
     npilist.append(npi)
for npi1 in npilist:
    browser=webdriver.Chrome("D:\chromedriver_win32\chromedriver")              #open chrome web browser
    browser.get("http://test.healthqrs.com/login")                              #load healthqrs website into the chrome browser
    emailid = browser.find_element_by_name("email")                             #find email element and enter email address
    emailid.send_keys('bj.yurkovich@gmail.com')
    inputElement= browser.find_element_by_xpath("//input[@type='password']")    #find password element and enter password
    inputElement.send_keys('freedom')  
    inputElement.send_keys(Keys.ENTER)                                          #simulates pressing enter key
    try:
        element = WebDriverWait(browser, 1000).until(
            EC.presence_of_element_located((By.ID, "search-form-container"))
        )                                                                       #waits until the browser loads the search page
    finally:
        print ""
    procedurecode=browser.find_element_by_id("procedure_value")                 #find the input element with procedure value and enter from npi list
    procedurecode.send_keys(npi1)
    try:                                                                        #wait until the browser can populate the search results
        element = WebDriverWait(browser, 1000).until(
            EC.presence_of_element_located((By.CLASS_NAME, "angucomplete-row"))
        )
    finally:
        print ""
    mouse = webdriver.ActionChains(browser)
    span_element = browser.find_element_by_class_name("angucomplete-row")
    mouse.move_to_element(span_element).click().perform()                      #click on the loaded search result
    #select= browser.find_element_by_xpath("//div[contains(@class, 'angucomplete-row')]")
    #select.click()
    zip1=browser.find_element_by_name("zip")                                   #find the zip code input element
    zip1.send_keys("70113")
    milerad= browser.find_element_by_xpath("//label[text()='100 mi']")         #click on the 100 mile radius button
    milerad.click()
    inputElement1= browser.find_element_by_xpath("//input[@type='submit']")
    inputElement1.click()
    #break
    try:                                                                        #wait until the browser can load the results
            element = WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-container"))
            )
    finally:
            print ""
    results= browser.find_elements_by_xpath("//button[contains(.,'Select')]")
    print len(results)
    i=0
    while i < len(results):                                                      #run the loop until the results are all tested
        results= browser.find_elements_by_xpath("//button[contains(.,'Select')]")   #maintain a list of button elements
        #but=result.find_element_by_xpath("//button[contains(.,'Select')]")
        results[i].click()                                                       #click on the button element depending upon the counter in the loop
        try:
                    element = WebDriverWait(browser, 1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ng-pristine"))
                    )
        finally:
                    print ""
        name_element = browser.find_element_by_name("name")             #fill in the credit card details
        name_element.send_keys("John Doe")
        address_element= browser.find_element_by_name("address")
        address_element.send_keys("1450 worthington street")
        city_element= browser.find_element_by_name("city")
        city_element.send_keys("Columbus")
        state_element= browser.find_element_by_name("states")
        state_element.send_keys("OH")
        zip_element= browser.find_element_by_name("zip")
        zip_element.send_keys("43201")
        cardno_element= browser.find_element_by_name("cc")
        cardno_element.send_keys("6011 0070 2132 8918")
        exp_element= browser.find_element_by_name("exp")
        exp_element.send_keys("12/19")
        ccv_element= browser.find_element_by_name("ccv")
        ccv_element.send_keys("836")
        terms_element= browser.find_element_by_name("terms").click()
        btn_element= browser.find_element_by_class_name("btn")
        btn_element.click()                         #click on the submit button and if the resulting web page contains "nav-menu-cotainer" print success
        try:
                            element = WebDriverWait(browser, 1000).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "nav-menu-container"))
                            )
        finally:
                            print "success"
        browser.back()
        i+=1
    
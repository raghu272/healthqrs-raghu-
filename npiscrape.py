import requests
from bs4 import BeautifulSoup
import xlrd
import selenium
import xlwt
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser=webdriver.Firefox()
browser.get("http://www.findacode.com/tools/npi-lookup.html")
mouse = webdriver.ActionChains(browser)
span_xpath = '//span[contains(text(), "Sign In")]'
span_element = browser.find_element_by_xpath(span_xpath)
mouse.move_to_element(span_element).click().perform()
helper=1
wb = xlwt.Workbook()                                                                 
while helper==1:
    try:
        emailid = browser.find_element_by_id("main_signin")
        emailid.send_keys('raghav.chhabra@gmail.com')
        inputElement = browser.find_element_by_name("password")
        inputElement.send_keys('anaklusmos@1')  
        inputElement.send_keys(Keys.ENTER)
        helper = 0
    except:
        helper = 1
def find_nth(haystack, needle, n):                                   #method to find the index of nth occurrence of a substring needle in a string haystack
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start
xl_workbook = xlrd.open_workbook("./myworkbook1.xls")
sheet_names = xl_workbook.sheet_names()
xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
col=xl_sheet.col(0)
count=0
ws = wb.add_sheet("My Sheet")
npi=[]
for name in col:
    if count==0:
        count+=1
        continue
    else:
        i=str(name)
        #print name
        docname=i[11:len(i)-5]
        #print docname
        if '.' in docname:
            fn=find_nth(docname,'.',1)
            #print fn
            firstname=docname[:fn-1]
            lastname=docname[fn+2:]
        else:
            fn=find_nth(docname,' ',1)
            firstname=docname[:fn]
            lastname=docname[fn+1:]
        #print firstname
        #print lastname
        fname = browser.find_element_by_id("name_first")
        fname.clear()
        fname.send_keys(firstname)
        lname = browser.find_element_by_id("name_last")
        lname.clear()
        lname.send_keys(lastname)
        state = browser.find_element_by_name("state")
        state.send_keys("LA")
        browser.find_element_by_id("results_any").click()
        sub = browser.find_element_by_name("submit")
        sub.submit()
        cnt=1
        while(cnt==1):
            x=browser.find_elements_by_xpath(("//table[@class='result_table']"))
            if len(x)>0:
                cnt=0
                a= x[0].text
                if firstname.upper() in a and lastname.upper() in a:
                    b=find_nth(a, firstname.upper(), 1)
                    temp= a[:b]
                    strt=len(temp)-45
                    temp=temp[strt:]
                    if "NPI" in temp:
                        strt=find_nth(temp,"NPI", 1)
                        print temp[strt+5:strt+15]
                        npi.append(temp[strt+5:strt+15])
                    else :
                        print "couldn't find doctor"
                        npi.append("couldn't find doctor")
                else :
                    print "couldn't find doctor"
                    npi.append("couldn't find doctor")                
i=0
t=0
col=col[1:]
for c in col:
    t = t+1
    ws.write(t, i, str(c))                                                            #writes to the work sheet
i=i+1
t=0 
for n in npi:
    t = t+1
    ws.write(t, i, n)                                                            #writes to the work sheet
i=i+1
t=0
wb.save("npi1.xls") 
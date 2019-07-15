from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import re


#project is still in progress, it will not parse all applicable pictures, but it will parse a number of pictures throughout the whole page.
imagedict = {}
numPics = 0

chromedriverlocation = 'D:\Dropbox\ProgrammingFiles\PythonScrape\chromedriver_win32\chromedriver.exe'
debug = True
wait_time = 0
if (debug):
    wait_time = 1.5

driver = webdriver.Chrome(chromedriverlocation)

url = 'http://www.instagram.com'
extendedurl = url + '/accounts/login/?source=auth_switcher' #this url helps ignore loginLink.click
driver.get(extendedurl)
#sleep(wait_time) #this is unnecessary due to using the extendedurl
#loginLink = driver.find_element_by_xpath("//a[text()='Log in']")
#loginLink.click()

user = 'scrape2019' #alternate: sinjzmaj@hotmail.com
password = 'instapass'

sleep(wait_time)
userInput = driver.find_element_by_name('username')
userInput.send_keys(user)
passInput = driver.find_element_by_name('password')
passInput.send_keys(password)

submitKey = driver.find_element_by_xpath("//button[@type='submit']")
submitKey.click()
sleep(wait_time)

ignore_notifications = driver.find_element_by_xpath("//button[text() = 'Not Now']")
ignore_notifications.click()


def soupnstore(page_source):

    instasoup = BeautifulSoup(page_source, 'lxml') #this may not work, may need requests first
    images = instasoup.find_all('img')
    for img in images:
        #this works imgCheck = re.compile(r'<img.*[^>]src.*[^>]style.*/>') #parsing tags would be an iteration, this just includes each without making a try except block
        imgcheck = re.compile(r'<img[^>]{1,}src[^>]{1,}style.*/>')
        if imgcheck.match(str(img)):
            picture = img['src']
            tag = img.parent
            parentcheck = re.compile(r'<div[^>]{1,}role.*/>')
            print(img)
            for parent in img.parents:
                if parentcheck.match(str(parent)):
                    tag = parent
                    break
            if tag.parent.next_sibling is not None:
                name = tag.parent.next_sibling.h2.next_sibling.span.string
                imagedict[name] = picture
            else:
                print('what was none:', tag.parent.parent.prettify())
        #now it needs to scroll down and store the files




rng = 100
initialTitle = driver.find_element_by_xpath("//h2/following-sibling::span/span")
xpathSelect = "//h2/following-sibling::span/span"
once = False
action = ActionChains(driver)
short_wait = 2
prevHeight = 0
initialrun = 2 #in case the run doesn't even start after the first rounds
body = driver.find_element_by_xpath('/html/body')
soupnstore(driver.page_source)
for i in range(0, rng):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    scrollHeight = driver.execute_script("return document.body.scrollHeight;")
    body.send_keys(Keys.PAGE_DOWN)
    if scrollHeight == prevHeight and initialrun < 0:
        break
    else:
        prevHeight = scrollHeight
    initialrun -= 1
    soupnstore(driver.page_source)
    sleep(short_wait)


    '''
    #driver.refresh()
    try:
        newelement = driver.find_element_by_xpath(xpathSelect)
    except exceptions.NoSuchElementException as exc:
        print(exc)
        print('ended at', xpathSelect)
        break
    text = newelement.text

    action.move_to_element(newelement)
    action.perform()
    sleep(short_wait)
    print(text)
    if not once:
        xpathSelect += "[text()!='" + text + "']"
        once = True
    else:
        newSelect = xpathSelect[0:(len(xpathSelect) - 1)]+" and "
        xpathSelect = newSelect + "text()!='" + text + "']"
    print(xpathSelect)
    '''
#this needs to be parsed slowly, different beautifulsoups for each portion of the web page apparently
print(imagedict.keys())
print('items found:', len(imagedict.keys()))
driver.close()

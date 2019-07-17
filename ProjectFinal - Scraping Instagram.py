from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from time import sleep


# issues: does not store the image to the hard disk, also does not parse a multi-image set
# timing could be improved by only parsing a page that has stored elements: the current process was simply parsing after scrolling down
# ways to scroll down: page down (what was used), navigate to element, down arrow
# also to test if the page is the same can filter through bs4
# you could test if the first element still exists and then move forward. This might be worth a try.


imagedict = {}


def findimages(page_source, imagedict):
    instasoup = BeautifulSoup(driver.page_source, 'lxml')  # this may not work, may need requests first
    srcsets = instasoup.select('img[srcset]')

    counter = 0
    print('new page search:')
    for img in srcsets:

        picture = img['src']
        tag = img.parent

        parentcheck = re.compile(r'<div[^>]{1,}role="button" tabindex="0">')

        for parent in img.parents:
            parentstring = str(parent)

            if (parent.has_attr('class')):  #
                if parent['class'].count('ZyFrc') > 0:
                    tag = parent
                    if tag.parent.parent.find('div', {'class': 'C4VMK'}) is not None:
                        print(tag.parent.parent.find('div', {'class': 'C4VMK'}).span.span.string.strip())
                        name = tag.parent.parent.find('div', {'class': 'C4VMK'}).span.span.string.strip()
                        imagedict[name] = picture


#here is getting to the instagram page
chromedriverlocation = 'D:\Dropbox\ProgrammingFiles\PythonScrape\chromedriver_win32\chromedriver.exe'
wait_time = 2

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

rng = 100
runcount = 0
runend = 3
prevHeight = 0
xpathSelect = "(//h2/following-sibling::span/span)[last()]"
lastelement = driver.find_element_by_xpath(xpathSelect)
for i in range(0, rng):
    runcount += 1
    findimages(driver.page_source, imagedict)
    body = driver.find_element_by_xpath('/html/body')
    body.send_keys(Keys.PAGE_DOWN)

    curlast = driver.find_element_by_xpath(xpathSelect)
    print(lastelement)
    if curlast == lastelement:
        runcount += 1
        if runcount > runend:
            break
    else:
        lastelement = curlast
        runcount = 0


print('all sampled pictures:')
for key in imagedict.keys():
    print(key)
driver.close()

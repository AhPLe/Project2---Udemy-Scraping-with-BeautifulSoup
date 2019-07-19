from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from time import sleep
import os
import requests
import shutil

# issues: this is fairly brittle. I don't know what the class encodings are or mean, but they work for this specific use
# all pictures need a caption. It would be fairly simple to reprogram this, but that is currently how it works
# parsing an album set currently partially works, but should be revised
# this will only store .jpg pictures from instagram, it will probably be a 'corrupt image' if a different type is stored


imagedict = {}
debug = True

def createfolder(name):
    #should test if directory exists
    if not os.path.isdir(name):
        os.mkdir(name)


def storeimages(imagedict):
    # this stores all files in the current directory. It should store files in a folder
    folder = 'instagrampics'
    createfolder(folder)
    for key in imagedict.keys():
        keyname = key + '.jpg'
        keyname = os.path.join(folder, keyname)
        response = requests.get(imagedict[key], stream=True, headers=header)
        with open(keyname, 'wb') as picture:
            shutil.copyfileobj(response.raw, picture)
        del response
        picture.close()
        print('picture stored at', keyname)

# this may be useless, the iteration over the parse tree will need to happen, and be able to take each image iterated over
# if this does not help with the image over a dictionary, it is not helpful
# def immediateimage(tag, imagedict, picture = None):
#    # from the image part of the class, get the name and picture of the tag
#    nametag = tag.select('div.ZyFrc')[0]
#    name = nametag.parent.parent.find('div', {'class': 'C4VMK'}).span.span.string.string.strip()
#    if picture is not None:
#        imagedict[name] = picture
#    else:
#        imagedict[name] = tag.select('img[srcset]')[0]


def find_right_album_button_by_tagname(righta_driver, tagname):
    elements = righta_driver.find_elements_by_css_selector('article._8Rm4L')
    for element in elements:
        captionlist = element.find_elements_by_xpath('//span[contains(text(), "{}")]'.format(tagname))
        if len(captionlist) > 0:
            # the element being searched is the correct base element to find things from
            right_button_list = element.find_elements_by_css_selector('button._6CZji')
            if len(right_button_list) > 0:
                return right_button_list[0]

    return None  # if there was no right button to find, this should be returned


def get_links_from_soup_album(page, tagname):
    # returns the links associated with the tagname
    links = []
    link_soup = BeautifulSoup(page, 'lxml')
    css_select = 'div.ZyFrc:contains("{}")'.format(tagname)
    outer_caption = link_soup.select(css_select)
    for parent in outer_caption[0].parents:
        if parent.has_attr('class') and parent['class'].count('_8Rm4L') > 0:
            soup_outer_tag = parent
            for link in soup_outer_tag.select('img[srcset]'):
                links.append(link['src'])
    return links


def getalbum(album_imagedict, album_driver, tagname):
    album_links = []
    page = album_driver.page_source
    count = 1
    hasnextbutton = True

    while hasnextbutton:  # this chooses the parse right button
        # gets the tag name of the picture
        page = album_driver.page_source
        for link in get_links_from_soup_album(page, tagname):
            # this probably produces duplicate links, there are usually two linked images per page for an album
            if album_links.count(link) < 1:
                album_imagedict[tagname + str(count)] = link
                count += 1
                album_links.append(link)

        # find the tagname using xpath
        nextimagebutton = find_right_album_button_by_tagname(album_driver, tagname)

        if nextimagebutton is not None:
            nextimagebutton.click()
        else:
            hasnextbutton = False


def findimages(page_source, images_imagedict):
    instasoup = BeautifulSoup(page_source, 'lxml')  # this may not work, may need requests first
    srcsets = instasoup.select('img[srcset]')

    counter = 0
    for img in srcsets:

        picture = img['src']
        tag = img.parent

        for parent in img.parents:

            if parent.has_attr('class') and parent['class'].count('_8Rm4L') > 0:  #
                # these represent a one picture frame. other classes for this tag were 'M9sTE' and 'L_LMM'

                tag = parent
                outer_tag_name = tag.select('div.ZyFrc')[0]

                if outer_tag_name.parent.parent.find('div', {'class': 'C4VMK'}) is not None:
                    if debug:
                        print(outer_tag_name.parent.parent.find('div', {'class': 'C4VMK'}).span.span.string.strip())
                    label = outer_tag_name.parent.parent.find('div', {'class': 'C4VMK'}).span.span.string.strip()

                    # first it needs to check if this tag has multiple pictures
                    if len(parent.select('button._6CZji')) > 0:
                        getalbum(images_imagedict, driver, label)

                    else:
                        images_imagedict[label] = picture


def start_driver():
    # here is getting to the instagram page
    chromedriverlocation = 'D:\Dropbox\ProgrammingFiles\PythonScrape\chromedriver_win32\chromedriver.exe'
    wait_time = 2

    startup_driver = webdriver.Chrome(chromedriverlocation)

    url = 'http://www.instagram.com'
    extendedurl = url + '/accounts/login/?source=auth_switcher' #this url helps ignore loginLink.click
    startup_driver.get(extendedurl)
    #sleep(wait_time) #this is unnecessary due to using the extendedurl
    #loginLink = driver.find_element_by_xpath("//a[text()='Log in']")
    #loginLink.click()

    user = 'username'
    password = 'password'

    sleep(wait_time)
    userInput = startup_driver.find_element_by_name('username')
    userInput.send_keys(user)
    passInput = startup_driver.find_element_by_name('password')
    passInput.send_keys(password)

    submitKey = startup_driver.find_element_by_xpath("//button[@type='submit']")
    submitKey.click()
    sleep(wait_time)

    ignore_notifications = startup_driver.find_element_by_xpath("//button[text() = 'Not Now']")
    ignore_notifications.click()
    return startup_driver


driver = start_driver()

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
    if curlast == lastelement:
        runcount += 1
        if runcount > runend:
            break
    else:
        lastelement = curlast
        runcount = 0

#storeimages(imagedict) for final version use this line and comment out next 3
print('all sampled pictures:')
for key in imagedict.keys():
    print(key)
storeimages(imagedict)
driver.close()

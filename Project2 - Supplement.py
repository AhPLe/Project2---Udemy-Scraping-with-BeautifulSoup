import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import fileinput
import get_html
'''
this file was intended to supplement an exercise to list all problems from 'codingbat.com'
the goal of this file was to store each individual parsed category and exercise and store them in folders
it is close to being used to completely print out each exercise problem, 
but this way modifications can be made without pinging the host site
this was intended to be used with Project2 - CodingBatExercises.py
'''


def read_file():
    location = 'CodingBat.txt'
    file = open(location)
    data = file.read()
    file.close()
    return data


def createFormat(newtext): #this is not necessary for this module, but it can be used for the project
    finalstring = ''
    finalstring += newtext.p.string
    newtext = newtext.next_sibling
    while (newtext.string is not None and newtext.name != 'p'):  # this should work
        finalstring += '\n' + newtext.string
        newtext = newtext.next_sibling
    return finalstring


url = 'https://codingbat.com/java'
fileName = 'CodingBat'
data = read_file()

soup = get_html.store_site(url, getsoup=True)

# from the soup, the find all class 'summ' and extract the href from the a tag below it.
attr = {'class': 'summ'}

div_tags = soup.find_all('div', attrs=attr)

categories = {}
once = False
additiveurl = url.rstrip('/java')
for div_tag in div_tags:
    catKey = div_tag.span.string
    categories[catKey] = div_tag.a['href']

    if not once:
        newSoup = get_html.store_site(additiveurl + div_tag.a['href'], catKey + '.txt', True, fileName)
        tdtags = newSoup.find_all('td', width=200) #this was a poor implementation, but it did work - should be managed through a larger tag

        for tdtag in tdtags:
            if not once:
                exercises = {}
                innerCatKey = tdtag.a.string
                innerNewSoup = get_html.store_site(additiveurl + tdtag.a['href'], \
                                                   innerCatKey + '.txt', True, fileName, catKey)
                categories[catKey] = tdtag.a.string

print(categories)
# need to search within tbodies, but use find all 'a' tags within, possibly going td - a
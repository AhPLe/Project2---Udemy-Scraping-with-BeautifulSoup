from bs4 import BeautifulSoup
import os
'''
this file was intended to list all problems from 'codingbat.com'
the goal was to print out (using write here) each exercise problem in a consistent format
this should be used with Project2 - Supplement.py, where the supplement extracts the files, and this reads them once stored
'''


def read_file(location = 'CodingBat.txt'):
    print('opening location:', location)
    file = open(location)
    data = file.read()
    file.close()
    return data


def createFormat(newtext):
    finalstring = ''
    firststrings = newtext.p.stripped_strings
    for astring in firststrings:
        finalstring += astring
    newtext = newtext.next_sibling
    while (newtext.string is not None and newtext.name != 'p'):
        finalstring += '\n' + newtext.string
        newtext = newtext.next_sibling
    return finalstring


url = 'https://codingbat.com/java'
fileName = 'CodingBat.txt'
#fileName.index('.')
fileLocation, _ = fileName.split('.txt')
print(fileLocation)
data = read_file(fileName)

soup = BeautifulSoup(data, 'lxml')

# from the soup, the find all class 'summ' and extract the href from the a tag below it.
attr = {'class': 'summ'}
div_tags = soup.find_all('div', attrs=attr)

categories = {}
once = False
for div_tag in div_tags:
    catKey = div_tag.span.string
    categories[catKey] = div_tag.a['href']

    newSoup = BeautifulSoup(read_file(os.path.join(fileLocation, catKey + '.txt')), 'lxml')
    tdtags = newSoup.find_all('td', width=200)
    exercises = {}

    for tdtag in tdtags:
        innerCatKey = tdtag.a.string
        innerNewSoup = BeautifulSoup(read_file(os.path.join(fileLocation, catKey, innerCatKey + '.txt')), 'lxml')
        problem = createFormat(innerNewSoup.find('div', class_='minh'))
        exercises[innerCatKey] = problem

    categories[catKey] = exercises

# undo once true parts, then go through site to check if each exerise was actually correct
print(categories)
with open(fileLocation + 'exercises.txt', 'w',  encoding='utf-8') as file:
    for lst1 in categories:
        file.write(lst1)
        file.write('\n')
        for problem in categories[lst1]:
            file.write(problem)
            file.write('\n')
            #print(categories[lst1][problem])
            file.write(categories[lst1][problem])
            file.write('\n\n')
    file.close()

# need to search within tbodies, but use find all 'a' tags within, possibly going td - a
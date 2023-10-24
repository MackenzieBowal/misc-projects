import requests
from bs4 import BeautifulSoup
import csv
import string
import re

# Scrape every Bible verse from the book of Genesis

alltext = []

for i in range(1, 51):

    url = 'https://biblegateway.com/passage/?search=Genesis%20{}&version=ESV'.format(i)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for paragroup in soup.find_all('p'):
        para = paragroup.get_text()
        if ("The Holy Bible" in para):
            break
        else:
            delimiters = r'[ \xa0]'
            words = re.split(delimiters, para)
            para = ' '.join(words)  # get rid of special spaces
            para = re.sub(r'[()\[].{1,3}[)\]]|\d', '', para)
            para = ' '.join(para.split())   # remove extra spaces
            alltext.append(para)

csv_filename = 'genesis.csv'

csvfile = open(csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csvfile)

i = 0
for sometext in alltext:
    if i > len(alltext) - 10:
        print(sometext, 0)
        continue
    i+=1
    csv_writer.writerow([sometext, 0])


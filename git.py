# -*- coding: utf-8 -*-
import requests
import commands
import os
from bs4 import BeautifulSoup
import fileinput
import sys 
import json
import sqlite3

reload(sys)    
sys.setdefaultencoding('utf-8') 
global conn
conn = sqlite3.connect('test.db')
f = open('new.html','w')
f.write('<html>')
f.write('<head><base href="https://github.com/"/></head>')  
r = requests.get('http://quan.suning.com/getSysTime.do')
nowTime = json.loads(r.text)['sysTime1']   

def load():
  global all_names
  all_names = set()  
  c = conn.cursor()
  cursor = c.execute("SELECT name from github_treading_table")
  for row in cursor:
    all_names.add(row[0]) 
  #print len(all_names)

def insert2DB( name, language, description, stars, date=0):    
  if stars.strip() == '':
    stars2 = 0
  else:
    stars2 = int(stars.replace(',', ''))  
  if stars2 < 10:
    return
  c = conn.cursor()
  c.execute("INSERT INTO github_treading_table VALUES (?, ?, ?, ?, ?)", \
     (name, language, description,stars2 , nowTime))
  conn.commit()  

def getItems(url, type='', lang=''):  
  requests.packages.urllib3.disable_warnings()
  r = requests.get(url, verify=False)
  r.encoding='utf-8'
  content = r.text
  soup = BeautifulSoup(content, 'lxml')
  items = {}
  for li in soup.find_all('article', class_="Box-row"):
    desc2=''
    address = li.find('h2', class_='h3 lh-condensed').a.get('href')  
    if address in all_names:
      continue    
    if li.p != None:
      try:
        desc2 = li.p.get_text().strip()
      except:
        print 'xx'
    
    stars1 =  li.find('div', class_='f6 color-fg-muted mt-2').a
    stars = ""
    if stars1 != None:
      stars = stars1.get_text().strip()
    lang=""
    language = li.find('div', class_='f6 color-fg-muted mt-2').find(name='span', attrs={"itemprop" :"programmingLanguage"})
    if language != None:
      lang =  language.get_text().strip()
    all_names.add(address)  

    insert2DB(address, lang, desc2, stars)  
    print address

    f.write('<a href="%s"><h >'%address+address+'</h></a>')
    f.write('<h>        '+lang+'</h>')
    f.write('<h>  '+stars+'</h>')  
    f.write('<br/>')
    f.write('<h>'+desc2+'</h>')  
    f.write('<hr/>')
  f.write('</html>')   
  
load()
url = 'https://github.com/trending?since=weekly'
since=['daily', 'weekly', 'monthly']
langs = ['','java', 'python', 'c++', 'html', 'css','typescript','javascript', 'php', 'ruby','perl','scala','rust', 'go', 'c', \
  'shell', 'kotlin', 'c%23', 'lua','haskell','unknown']
for date in since:
  for lang in langs:
    url = 'https://github.com/trending/%s?since=%s'%(lang, date)
    print url
    getItems(url)
conn.close()
f.close()

# -*- coding: utf-8 -*-

import sqlite3

import sys



reload(sys)    

sys.setdefaultencoding('utf-8') 



conn = sqlite3.connect('test.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS github_treading_table

       (name TEXT PRIMARY KEY     NOT NULL,

        language           TEXT,

        description        TEXT,

        stars        INT NOT NULL,

        date         INTEGER  NOT NULL);''')



f = open('index.html','w')

f.write('<html>') 

f.write('<head><base href="https://github.com/"/></head>') 

cursor = c.execute("SELECT name, language, description, stars, date from github_treading_table ORDER BY stars DESC")

for row in cursor:

  print 'name=', row[0]

  print 'language=', row[1]

  #print 'description=', row[2]

  print 'stars=', row[3]

  print 'date=', row[4]

  

  f.write('<a href="%s"><h >'%row[0]+row[0]+'</h></a>')

  f.write('<h>        '+row[1]+'</h>')

  f.write('<h>  '+str(row[3])+'</h>')  

  f.write('<br/>')

  f.write('<h>'+row[2]+'</h>')  

  f.write('<hr/>')

f.write('</html>')  

  

f.close()

conn.commit()

conn.close()



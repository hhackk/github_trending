# -*- coding: utf-8 -*-

import sqlite3

import sys
from github import Github

g = Github("1f83e7f8b0d9ee4f1172e415b749ba55b1c2b82e")
#repo = g.get_repo("PyGithub/PyGithub")
#print repo.created_at

def escape(s):
  s = s.replace("&", "&amp;")
  s = s.replace("<", "&lt;")
  s = s.replace(">", "&gt;")
  return s

#reload(sys)    

#sys.setdefaultencoding('utf-8') 



conn = sqlite3.connect('test.db')

c = conn.cursor()



f = open('index.html','w')

f.write('<html>') 

f.write('<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>自动跟踪最热github项目 --by gcf</title><style type="text/css">a {text-decoration: none} body{background-color:#EBEBE4}</style><base href="https://github.com/"/></head>') 

cursor = c.execute("SELECT name, language, description, stars, date from github_treading_table ORDER BY date DESC,stars DESC LIMIT 90")

for row in cursor:

  print('name=', row[0])

  #print 'language=', row[1]

  #print 'description=', row[2]

  #print 'stars=', row[3]

  #print 'date=', row[4]

  
  mydate = str(row[4])

  f.write('<h>'+mydate[4:6] + '-' + mydate[6:8] + ' ' + mydate[8:10] + ':' + mydate[10:12] +'&nbsp;&nbsp;&nbsp;&nbsp;</h>')
  f.write('<a href="%s"><h >'%row[0]+row[0]+'</h></a>')

  f.write('<h>        '+escape(row[1])+'</h>')

  #f.write('<h>  '+str(row[3])+'</h>')  
  f.write('<a href="https://starchart.cc'+row[0] + '.svg">  '+str(row[3])+'</a>')

  try:
    repo = g.get_repo(str(row[0])[1:])
  
    f.write('<h>   '+repo.created_at.strftime('%Y-%m-%d')+'</h>')
  except :
    pass
  f.write('<br/>')
  f.write('<h>   '+escape(row[2])+'</h>')  


  f.write('<hr/>')
f.write('</html>')  

  

f.close()

conn.commit()

conn.close()

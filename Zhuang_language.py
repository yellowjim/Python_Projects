# -*- coding:utf-8 -*-
import urllib2
import urllib
import mysql.connector
import re

dic={'那','Naz'}

def choose_word(word):
    temp_l=[]
    temp_dic={}
    for x in word:
        len_word=len(x)
        temp_l.append(len_word)
        temp_dic[len(x)]=x
    temp_l.sort()
    return temp_dic[temp_l[0]].capitalize()

ip=raw_input()
db={}
dmpc = mysql.connector.connect(user='root', password='GwGcgx@2016!',host=ip, database='dmpc1', use_unicode=True)
cursor = dmpc.cursor()
cursor.execute("SELECT f_id,f_name,f_nationalname from v_xingning where f_language='壮语' and f_nationalname=''")
data=cursor.fetchall()
for f_id,f_name,f_nationalname in data:
    db[f_id]=(f_name,f_nationalname)
cursor.close()
dmpc.close()
for x in db:
    print db[x]

p=re.compile('\\r\\n\\t\\t([a-z]+)\\t\\t')
data = {'cih': '', 'js': '岭','t1':'提交'}
post = urllib2.urlopen(
        url= 'http://www.jiu60.com/hoiz/sawl.asp',
        data= urllib.urlencode(data))
l_word=p.findall(post.read())
print choose_word(l_word)  #壮语译写首字母大写

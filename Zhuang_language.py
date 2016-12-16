# -*- coding:utf-8 -*-
import urllib2
import urllib
import mysql.connector

l=[]
dmpc = mysql.connector.connect(user='root', password='GwGcgx@2016!',host='10.1.10.169', database='dmpc1', use_unicode=True)
cursor = dmpc.cursor()
query = ("SELECT f_name from v_xingning where f_language='壮语'")
cursor.execute(query)
print cursor

dmpc.close()


# data = {'cih' : '', 'js' : '那','t1':'提交'}
# f = urllib2.urlopen(
#         url= 'http://www.jiu60.com/hoiz/sawl.asp',
#         data= urllib.urlencode(data))
# print f.read()
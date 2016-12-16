# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import urllib
import mysql.connector
import re
import csv
import os
from Tkinter import *

c_path=os.getcwd()+'\\'
db_place = {}
dic_zhuangyu={u'那':'Naz'}
p=re.compile('\\r\\n\\t\\t([a-z]+)\\t\\t')

# def db2csv(guid,id,name,word):
#     with open(c_path+u'壮语地名书写.csv', 'w+') as csvfile:
#         fieldnames = [u'GUID', u'FeatureID',u'标准名称',u'壮语书写']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerow({u'GUID':guid, u'FeatureID':id,u'标准名称':name,u'壮语书写':word})
#         csvfile.close()

def choose_word(word,flag):
    temp_dic={}
    for x in word:
        len_word=len(x)
        temp_dic[len(x)]=x
    temp_dic=sorted(temp_dic.iteritems(), key=lambda d: d[0], reverse=False)
    if flag==1:
        return temp_dic[0][1].capitalize()
    else:
        return temp_dic[0][1]


def query_word(word,flag):
    if dic_zhuangyu.has_key(word) and flag==1:
        return dic_zhuangyu[word].capitalize()
    elif dic_zhuangyu.has_key(word) and flag!=1:
        return dic_zhuangyu[word]
    else:
        js=word.encode('utf-8')
        post_data = {'cih': '', 'js': js, 't1': '提交'}
        post = urllib2.urlopen(url= 'http://www.jiu60.com/hoiz/sawl.asp',data= urllib.urlencode(post_data))
        l_word=p.findall(post.read())
        if l_word==[]:
            return ''
        elif flag==1:
            return choose_word(l_word,1)
        else:
            return choose_word(l_word,0)

def main():
    try:
        os.remove(c_path+u'壮语地名书写.csv')
    except:
        pass
    ip=raw_input("输入IP地址：")
    dmpc = mysql.connector.connect(user='root', password='GwGcgx@2016!',host=ip, database='dmpc1', use_unicode=True)
    cursor = dmpc.cursor()
    cursor.execute("SELECT f_id,f_idcode,f_name,f_nationalname from v_xingning where f_language='壮语' and f_name like '那%'")
    data=cursor.fetchall()
    for f_id,f_idcode,f_name,f_nationalname in data:
        db_place[f_id]=(f_idcode,f_name,f_nationalname)
    for place in db_place:
        for sub_word in db_place[place][1]:
            if db_place[place][0][1]==sub_word:
                # db2csv(place,db_place[place][0],db_place[place][1],db_place[place][2]+query_word(sub_word,1))
                db_place[place]=(db_place[place][0],db_place[place][1],db_place[place][2]+query_word(sub_word,1))
            else:
                # db2csv(place, db_place[place][0], db_place[place][1], db_place[place][2] + query_word(sub_word, 1))
                db_place[place] = (db_place[place][0],db_place[place][1], db_place[place][2] + query_word(sub_word, 0))
        print place, db_place[place][0], db_place[place][1],db_place[place][2]
        guid=place
        shuxie=db_place[place][2]
        cursor.execute("update v_xingning  set f_nationalname=%s where f_id=%s",(shuxie,guid))
        dmpc.commit()
    cursor.close()
    dmpc.close()

if __name__ == '__main__':
    main()

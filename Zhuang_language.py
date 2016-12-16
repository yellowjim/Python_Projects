# -*- coding:utf-8 -*-
import urllib2
import urllib
import mysql.connector
import re
import csv
from Tkinter import *

db_place = {}
dic_zhuangyu={u'那':'Naz'}
p=re.compile('\\r\\n\\t\\t([a-z]+)\\t\\t')

def choose_word(word,flag):
    temp_dic={}
    for x in word:
        len_word=len(x)
        temp_dic[len(x)]=x
    temp_dic=sorted(temp_dic.iteritems(), key=lambda d: d[0], reverse=False)
    print temp_dic
    if flag==1:
        for i,line in enumerate(temp_dic):
            if i==1:
                return temp_dic[i].capitalize()
    else:
        for i,line in enumerate(temp_dic):
            if i==1:
               return temp_dic[i]

def commit_ip(ipa):
    ip=ipa
    print ip

def query_word(word,flag):
    if dic_zhuangyu.has_key(word) and flag==1:
        return dic_zhuangyu[word].capitalize()
    elif dic_zhuangyu.has_key(word) and flag!=1:
        return dic_zhuangyu[word]
    else:
        js=word.encode('utf-8')
        post_data = {'cih': '', 'js': js, 't1': '提交'}
        post = urllib2.urlopen(
                url= 'http://www.jiu60.com/hoiz/sawl.asp',
                data= urllib.urlencode(post_data))
        l_word=p.findall(post.read())
        if word==[]:
            return ''
        elif flag==1:
            return choose_word(l_word,1)
        else:
            return choose_word(l_word,0)

def main():
    ip=raw_input("输入IP地址：")
    dmpc = mysql.connector.connect(user='root', password='GwGcgx@2016!',host=ip, database='dmpc1', use_unicode=True)
    cursor = dmpc.cursor()
    cursor.execute("SELECT f_id,f_name,f_nationalname from v_xingning where f_language='壮语' and f_name like '那%'")
    data=cursor.fetchall()
    for f_id,f_name,f_nationalname in data:
        db_place[f_id]=(f_name,f_nationalname)
    for place in db_place:
        for sub_word in db_place[place][0]:
            if db_place[place][0][0]==sub_word:
                db_place[place]=(db_place[place][0],db_place[place][1]+query_word(sub_word,1))
            else:
                db_place[place] = (db_place[place][0], db_place[place][1] + query_word(sub_word, 0))
        print db_place[place]
    cursor.close()
    dmpc.close()
    for place in db_place:
        print db_place[place][1]

if __name__ == '__main__':
    main()

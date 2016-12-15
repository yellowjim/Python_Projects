# -*- coding:utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os
import re
import sqlite3
db={}

def make_db_data(file_name,mode):
    if mode=='guid':
        if re.match('\d{6,}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_name from tb_landmark_info").fetchall()
            db_conn.close()
            for x in temp:
                if x[0]=='':
                    continue
                db[x[0]] = x[1]
        elif re.match(r'F\d{2}[a-zA-Z]{1}\d{6}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_name from tb_place_info").fetchall()
            db_conn.close()
            for x in temp:
                if x[0]=='':
                    continue
                db[x[0]] = x[1]
    elif mode=='fid':
        if re.match('\d{6,}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_name from tb_landmark_info").fetchall()
            db_conn.close()
            for x in temp:
                if x[0]=='':
                    continue
                db[x[0]] = x[1]
        elif re.match(r'F\d{2}[a-zA-Z]{1}\d{6}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_idcode,f_name from tb_place_info").fetchall()
            db_conn.close()
            for x in temp:
                if x[0] == '' and x[1] == '':
                    continue
                elif x[0] != '' and x[1] == '':
                    db[x[0]] = x[2]
                db[x[0]] = x[1]
                db[x[1]] = x[2]

def change_picname(old_name,mode):
    global guid
    global place_start
    global landmark_start
    if mode=='guid':
        if os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{32}').search(old_name):
            c_guid=re.compile('[0-9a-zA-Z]{32}').search(old_name).group()
            if c_guid==guid and place_start<10:
                try:
                    pic_name=db[c_guid]+'0'+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    place_start += 1
                except:
                    pass
            elif c_guid != guid:
                try:
                    place_start = 1
                    pic_name=db[c_guid]+'0'+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    place_start+= 1
                    guid=c_guid
                except:
                    pass
        elif os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{16}').search(old_name):
            c_guid=re.compile('[0-9a-zA-Z]{16}').search(old_name).group()
            if c_guid==guid and landmark_start<20:
                try:
                    pic_name=db[c_guid]+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    landmark_start+=1
                except:
                    pass
            elif c_guid!=guid:
                try:
                    landmark_start = 11
                    pic_name=db[c_guid]+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    landmark_start += 1
                    guid=c_guid
                except:
                    pass
    elif mode=='fid':
        if os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{32}').search(old_name):
            c_guid=re.compile('[0-9a-zA-Z]{32}').search(old_name).group()
            if c_guid==guid and place_start<10:
                try:
                    pic_name=db[db[c_guid]]+'0'+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    place_start += 1
                except:
                    pass
            elif c_guid != guid:
                try:
                    place_start = 1
                    pic_name=db[db[c_guid]]+'0'+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    place_start+= 1
                    guid=c_guid
                except:
                    pass
        elif os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{16}').search(old_name):
            c_guid=re.compile('[0-9a-zA-Z]{16}').search(old_name).group()
            if c_guid==guid and landmark_start<20:
                try:
                    pic_name=db[c_guid]+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    landmark_start+=1
                except:
                    pass
            elif c_guid!=guid:
                try:
                    landmark_start = 11
                    pic_name=db[c_guid]+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    try:
                        os.rename(old_name,new_name)
                    except:
                        pass
                    landmark_start += 1
                    guid=c_guid
                except:
                    pass

def guid_mode():
    global root
    global pic_path
    global db_path
    pic_path = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择【 照 片 （*.JPG） 】所在文件夹')
    while pic_path=='':
        return 0
    db_path=tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择【Sqlite数据库(*.db)】文件所在文件夹')
    while db_path=='':
        return 0
    if db_path==pic_path:
        for rootdir,dirs,files in os.walk(db_path):
            for files_name in files:
                make_db_data(os.path.join(rootdir,files_name),'guid')
        for rootdir,dirs,files in os.walk(pic_path):
            for files_name in files:
                change_picname(os.path.join(rootdir,files_name),'guid')
    else:
        for rootdir,dirs,files in os.walk(pic_path):
            for files_name in files:
                make_db_data(os.path.join(rootdir,files_name),'guid')
        for rootdir,dirs,files in os.walk(db_path):
            for files_name in files:
                make_db_data(os.path.join(rootdir,files_name),'guid')
        for rootdir,dirs,files in os.walk(pic_path):
            for files_name in files:
                change_picname(os.path.join(rootdir,files_name),'guid')
    tkMessageBox.showinfo(title='', message='照片更名完毕！')

def featureid_mode():
    global root
    global pic_path
    global db_path
    pic_path = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择【 照 片 （*.JPG） 】所在文件夹')
    while pic_path=='':
        return 0
    db_path=tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择从【运维平台】上下载的\n【Sqlite数据库(*.db)】文件所在文件夹')
    while db_path=='':
        return 0
    for rootdir,dirs,files in os.walk(pic_path):
        for files_name in files:
            make_db_data(os.path.join(rootdir,files_name),'fid')
    for rootdir,dirs,files in os.walk(db_path):
        for files_name in files:
            make_db_data(os.path.join(rootdir,files_name),'fid')
    for rootdir,dirs,files in os.walk(pic_path):
        for files_name in files:
            change_picname(os.path.join(rootdir,files_name),'fid')
    tkMessageBox.showinfo(title='', message='照片更名完毕！')

def main():
    global root
    global pic_path
    global db_path
    root = Tk()
    root.title('地名普查外业照片批量更名工具 Ver_1.0  YellowJim制作')
    Button(root,text = u'GUID 模式\n\n( 此模式适合GUID没有发生变化时 )',command=guid_mode,width = 70,height = 4,font='微软雅黑').pack()
    Button(root, text=u'FeatureID 模式\n\n( 此模式适合GUID发生变化，改用FeatureID匹配 )', command=featureid_mode, width=70, height=4,font='微软雅黑').pack()
    root.update()
    scnWidth,scnHeight = root.maxsize()
    tmpcnf = '%dx%d+%d+%d'%(480,200,(scnWidth-480)/2,(scnHeight-200)/2)
    root.geometry(tmpcnf)
    root.mainloop()

if __name__ == '__main__':
    global guid
    global place_start
    global landmark_start
    global pic_path
    global db_path
    place_start=1
    landmark_start=11
    guid=''
    pic_path=''
    db_path=''
    main()
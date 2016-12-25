# -*- coding:utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os
import re
import sqlite3
import csv, codecs, cStringIO
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

place_start=11
landmark_start=1
guid=''
pic_path=''
db_path=''
db={}
output_file=''

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def output_csv():
    global db
    global output_file
    with open(output_file, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([u'是否拍照'.decode('utf-8').encode('MBCS'),u'类型'.decode('utf-8').encode('MBCS'),u'标识码'.decode('utf-8').encode('MBCS'),u'对比数据库来源'.decode('utf-8').encode('MBCS'),u'标准名称'.decode('utf-8').encode('MBCS'),u'地名大类代码'.decode('utf-8').encode('MBCS'),u'地名中类代码'.decode('utf-8').encode('MBCS'),u'经度'.decode('utf-8').encode('MBCS'),u'纬度'.decode('utf-8').encode('MBCS')])
        for x in db:
            if len(x)==16:
                csvWriter.writerow([db[x][-1].decode('utf-8').encode('MBCS'),u'地名标志'.decode('utf-8').encode('MBCS'),x,db[x][0].decode('utf-8').encode('MBCS'),db[x][2].decode('utf-8').encode('MBCS'),db[x][3],db[x][4],db[x][5],db[x][6]])
            if len(x)==32:
                csvWriter.writerow([db[x][-1].decode('utf-8').encode('MBCS'),u'地理实体'.decode('utf-8').encode('MBCS'),x,db[x][0].decode('utf-8').encode('MBCS'),db[x][2].decode('utf-8').encode('MBCS'),db[x][3],db[x][4],db[x][5],db[x][6]])
        csvFile.close()
        os.system(output_file.decode('utf-8').encode('MBCS'))

def make_db_data(file_name,mode,flag):
    global db
    print u'======================正在初始化，请耐心等候。。。======================'
    if mode=='guid':
        if re.match('\d{6,}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_idcode,f_name,f_lon,f_lat from tb_landmark_info order by f_placetype").fetchall()
            if temp:
                for x in temp:
                    db.update({x[0]:[flag,x[1],x[2],'','',x[3],x[4],u'漏拍']})
            db_conn.close()
        elif re.match(r'F\d{2}[a-zA-Z]{1}\d{6}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_idcode,f_name,f_firsttype,f_secondtype,f_lon,f_lat from tb_place_info order by f_firsttype,f_secondtype").fetchall()
            if temp:
                for x in temp:
                    db.update({x[0]:[flag,x[1],x[2],x[3],x[4],x[5],x[6],u'漏拍']})
            db_conn.close()
    elif mode=='fid':
        if re.match('\d{6,}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_idcode,f_name,f_lon,f_lat from tb_landmark_info order by f_placetype").fetchall()
            if temp:
                for x in temp:
                    db.update({x[0]:[flag,x[1],x[2],'','',x[3],x[4],u'漏拍']})
            db_conn.close()
        elif re.match(r'F\d{2}[a-zA-Z]{1}\d{6}.db$',os.path.basename(file_name)):
            db_conn = sqlite3.connect(file_name)
            db_cursor = db_conn.cursor()
            temp=db_cursor.execute("select f_id,f_idcode,f_name,f_firsttype,f_secondtype,f_lon,f_lat from tb_place_info order by f_firsttype,f_secondtype").fetchall()
            if temp:
                for x in temp:
                    db.update({x[0]:[flag,x[1],x[2],x[3],x[4],x[5],x[6],u'漏拍']})
                    db.update({x[1]:[flag,x[0],x[2],x[3],x[4],x[5],x[6],u'漏拍']})
            db_conn.close()

def change_picname(old_name,mode):
    global guid
    global place_start
    global landmark_start
    global sum_place
    global sum_place_pic
    global sum_landmark
    global sum_landmark_pic
    if mode=='guid':
        if os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{32}').search(old_name):
            sum_place_pic += 1
            c_guid=re.compile('[0-9a-zA-Z]{32}').search(old_name).group()
            if c_guid==guid and place_start<19:
                try:
                    pic_name=db[c_guid][2]+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    place_start += 1
                except:
                    pass
            elif c_guid != guid:
                sum_place+=1
                try:
                    place_start = 11
                    pic_name=db[c_guid][2]+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    place_start+= 1
                    db[c_guid][-1]=u'有照片'
                except:
                    pass
                guid=c_guid
        elif os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{16}').search(old_name) and (not re.compile('[0-9a-zA-Z]{32}').search(old_name)):
            sum_landmark_pic+=1
            c_guid=re.compile('[0-9a-zA-Z]{16}').search(old_name).group()
            if c_guid==guid and landmark_start<9:
                try:
                    pic_name=db[c_guid][2]+'0'+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    landmark_start+=1
                except:
                    pass
            elif c_guid!=guid:
                sum_landmark+=1
                try:
                    landmark_start = 1
                    pic_name=db[c_guid][2]+'0'+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    landmark_start += 1
                    db[c_guid][-1]=u'有照片'
                except:
                    pass
                guid=c_guid
    elif mode=='fid':
        if os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{32}').search(old_name):
            sum_place_pic+=1
            c_guid=re.compile('[0-9a-zA-Z]{32}').search(old_name).group()
            if c_guid==guid and place_start<19:
                try:
                    pic_name=db[db[c_guid][0]][2]+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    place_start += 1
                except:
                    pass
            elif c_guid != guid:
                sum_place+=1
                try:
                    place_start = 11
                    pic_name=db[db[c_guid][0]][2]+str(place_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    place_start+= 1
                    db[c_guid][-1]=u'有照片'
                except:
                    pass
                guid=c_guid
        elif os.path.splitext(old_name)[1].lower()=='.jpg' and re.compile('[0-9a-zA-Z]{16}').search(old_name) and (not re.compile('[0-9a-zA-Z]{32}').search(old_name)):
            sum_landmark_pic+=1
            c_guid=re.compile('[0-9a-zA-Z]{16}').search(old_name).group()
            if c_guid==guid and landmark_start<9:
                try:
                    pic_name=db[c_guid[0]][2]+'0'+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    landmark_start+=1
                except:
                    pass
            elif c_guid!=guid:
                sum_landmark +=1
                try:
                    landmark_start = 1
                    pic_name=db[c_guid[0]][2]+'0'+str(landmark_start)+'.jpg'
                    new_name=os.path.join(os.path.split(old_name)[0],pic_name)
                    print old_name.split('\\')[-1]+u'  更名为  '+pic_name
                    os.rename(old_name,new_name)
                    landmark_start += 1
                    db[c_guid][-1]=u'有照片'
                except:
                    pass
                guid=c_guid

def guid_mode():
    global db
    global output_file
    global L_pic
    global sum_place
    global sum_place_pic
    global sum_landmark
    global sum_landmark_pic
    global root
    global pic_path
    global db_path
    sum_place,sum_landmark,sum_place_pic,sum_landmark_pic=0,0,0,0
    L_pic=[]
    pic_path = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择【 照 片 （*.JPG） 】所在文件夹')
    while pic_path=='':
        return 0
    db_path=tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择【Sqlite数据库(*.db)】文件所在文件夹')
    while db_path=='':
        return 0
    output_file = tkFileDialog.asksaveasfilename(filetypes=[('CSV file', '.csv'), ('All files', '*')], title='请选择统计结果存放位置\n注:若无漏拍照片则表格为空',defaultextension='.csv')
    if output_file=='':
        return 0
    if db_path==pic_path:
        for rootdir,dirs,files in os.walk(db_path):
            for files_name in files:
                make_db_data(os.path.join(rootdir,files_name),'guid','照片文件夹数据库')
        for rootdir,dirs,files in os.walk(pic_path):
            for files_name in files:
                change_picname(os.path.join(rootdir,files_name),'guid')
    else:
        for rootdir,dirs,files in os.walk(pic_path):
            for files_name in files:
                make_db_data(os.path.join(rootdir,files_name),'guid','照片文件夹数据库')
        for rootdir,dirs,files in os.walk(db_path):
            for files_name in files:
                make_db_data(os.path.join(rootdir,files_name),'guid','平台数据库')
        for rootdir,dirs,files in os.walk(pic_path):
            for files_name in files:
                change_picname(os.path.join(rootdir,files_name),'guid')
    print u'共【 '+str(sum_place+sum_landmark)+u' 】个地名和【 '+str(sum_place_pic+sum_landmark_pic)+u' 】张照片\n地理实体：【 '+str(sum_place)+u' 】个，照片【 '+str(sum_place_pic)+u' 】张\n地名标志：【 '+str(sum_landmark)+u' 】个，照片【 '+str(sum_landmark_pic)+u' 】张'
    output_csv()

def featureid_mode():
    global db
    global output_file
    global sum_place
    global sum_place_pic
    global sum_landmark
    global sum_landmark_pic
    global root
    global pic_path
    global db_path
    sum_place,sum_landmark,sum_place_pic,sum_landmark_pic=0,0,0,0
    pic_path = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择【 照 片 （*.JPG） 】所在文件夹')
    if pic_path=='':
        return 0
    db_path=tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择从【运维平台】上下载的\n【Sqlite数据库(*.db)】文件所在文件夹')
    while pic_path in db_path:
        tkMessageBox.showinfo(title='警告', message='FeatureID模式下Sqlite数据库文件(*.db)文件\n不能放在外业照片的目录树中')
        db_path=tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择从【运维平台】上下载的\n【Sqlite数据库(*.db)】文件所在文件夹')
    if db_path=='':
        return 0
    output_file = tkFileDialog.asksaveasfilename(filetypes=[('CSV file', '.prj'), ('All files', '*')], title='请选择统计结果存放位置\n注:若无漏拍照片则表格为空',defaultextension='.csv')
    if output_file=='':
        return 0
    for rootdir,dirs,files in os.walk(pic_path):
        for files_name in files:
            make_db_data(os.path.join(rootdir,files_name),'fid','照片文件夹数据库')
    for rootdir,dirs,files in os.walk(db_path):
        for files_name in files:
            make_db_data(os.path.join(rootdir,files_name),'fid','平台数据库')
    for rootdir,dirs,files in os.walk(pic_path):
        for files_name in files:
            change_picname(os.path.join(rootdir,files_name),'fid')
    print u'共【 '+str(sum_place+sum_landmark)+u' 】个地名和【 '+str(sum_place_pic+sum_landmark_pic)+u' 】张照片\n地理实体：【 '+str(sum_place)+u' 】个，照片【 '+str(sum_place_pic)+u' 】张\n地名标志：【 '+str(sum_landmark)+u' 】个，照片【 '+str(sum_landmark_pic)+u' 】张'
    output_csv()

def main():
    global root
    global pic_path
    global db_path
    root = Tk()
    root.title('地名普查外业照片检查预处理工具 Ver_1.0 Made by 黄竣')
    Button(root,text = u'GUID 模式\n\n( 此模式适合GUID没有发生变化时 )',command=guid_mode,width = 70,height = 4,font='微软雅黑').pack()
    Button(root, text=u'FeatureID 模式\n\n( 此模式适合GUID发生变化，改用FeatureID匹配 )', command=featureid_mode, width=70, height=4,font='微软雅黑').pack()
    root.update()
    scnWidth,scnHeight = root.maxsize()
    tmpcnf = '%dx%d+%d+%d'%(480,200,(scnWidth-480)/2,(scnHeight-200)/2)
    root.geometry(tmpcnf)
    root.mainloop()

if __name__ == '__main__':
    main()
# -*- coding:utf-8 -*-
import csv
import exifread
from tkinter import *
import tkFileDialog
import os

dic_exif={}

def output_csv():
    global dic_exif
    global output_file
    with open(output_file, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        for x in dic_exif:
            csvWriter.writerow([x,dic_exif[x][0],dic_exif[x][1],dic_exif[x][2]])
        csvFile.close()


def getexif(pic):
    global dic_exif
    f = open(pic, 'rb')
    tags = exifread.process_file(f)
    pic_name=str(tags['Image ImageDescription']).split('\\')[-1]
    temp_lon=str(tags['GPS GPSLongitude'])[1:-1].split(',')
    temp_lat = str(tags['GPS GPSLatitude'])[1:-1].split(',')
    temp_Altitude=str(tags['GPS GPSAltitude']).split('/')
    Lon=float(temp_lon[0])+float(temp_lon[1])/60+float(temp_lon[2].split('/')[0])/float(temp_lon[2].split('/')[1])/3600
    Lat=float(temp_lat[0])+float(temp_lat[1])/60+float(temp_lat[2].split('/')[0])/float(temp_lat[2].split('/')[1])/3600
    Altitude=float(temp_Altitude[0])/float(temp_Altitude[1])
    print pic_name,Lon,Lat,Altitude
    dic_exif.update({pic_name:[Lon,Lat,Altitude]})
    f.close()
    output_csv()


def selectPath():
    global dic_exif
    global output_file
    dic_exif={}
    path_ = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择照片路径')
    path.set(path_)
    output_file = tkFileDialog.asksaveasfilename(filetypes=[('CSV file', '.csv'), ('All files', '*')],title='请选择结果存放位置', defaultextension='.csv')
    if os.path.isfile(output_file):
        os.remove(output_file)
    for rootdir, dirs, files in os.walk(path_):
        for files_name in files:
            getexif(os.path.join(rootdir, files_name))
    os.system(output_file.decode('utf-8').encode('MBCS'))

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


def main():
    global root
    global path_
    global path
    root = Tk()
    root.title('EXIF处理工具(DJI版)')
    center_window(root, 330, 35)
    path = StringVar()
    Label(root,text = "目标路径:").grid(row = 0, column = 0)
    Entry(root, textvariable = path).grid(row = 0, column = 1)
    Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)
    root.mainloop()

if __name__ == '__main__':
    main()
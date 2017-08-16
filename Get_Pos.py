# -*- coding:utf-8 -*-
import csv
from tkinter import *
import tkFileDialog
import os

dic_pos = {}
flag = 0
temp_name = ''
output_file=''


def output_csv():
    global dic_pos
    global output_file
    if output_file=='':
        return 0
    with open(output_file, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Path', 'X', 'Y', 'Altitude', 'Omega', 'Phi', 'Kappa'])
        for x in dic_pos:
            csvWriter.writerow(
                [x, dic_pos[x][0], dic_pos[x][1], dic_pos[x][2], dic_pos[x][3], dic_pos[x][4], dic_pos[x][5]])
        csvFile.close()


def getpos(path):
    global flag
    global dic_pos
    global temp_name
    command = r'exiftool -n -GPSLongitude -GPSLatitude -GPSAltitude -CameraRoll -CameraPitch -CameraYaw ' + path  # -n 参数表示输出双精度型
    r = os.popen(command)  # 执行该命令
    info = r.readlines()  # 读取命令行的输出到一个list
    count = len(info)
    for index, item in enumerate(info):
        if index == count - 2:
            break
        elif index % 7 == 0:
            flag = index
            pic_name = item.strip('\r\n').replace('======== ', '')
            temp_name = pic_name
            dic_pos[pic_name] = []
        else:
            pos_info = item.strip('\r\n')[34:]  # 34之后跟数值，之前的字符串是标签
            dic_pos[temp_name].append(pos_info)
    output_csv()


def selectpath():
    global dic_pos
    global output_file
    dic_pos = {}
    path_ = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择照片路径')
    if path_ == '':
        return 0
    path.set(path_)
    output_file = tkFileDialog.asksaveasfilename(filetypes=[('CSV file', '.csv'), ('All files', '*')],
                                                 title='请选择结果存放位置', defaultextension='.csv')
    if output_file=='':
        path.set('请选择照片路径')
        return 0
    if os.path.isfile(output_file):
        os.remove(output_file)
    getpos(path_)
    os.system(output_file)
    path.set('Pos信息提取完毕！')


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


def main():
    global output_file
    global root
    global path_
    global path
    root = Tk()
    root.title('EXIF_POS提取工具(DJI版)')
    center_window(root, 328, 35)
    path = StringVar()
    Label(root, text="目标路径:").grid(row=0, column=0)
    Entry(root, textvariable=path).grid(row=0, column=1)
    Button(root, text="路径选择", command=selectpath).grid(row=0, column=2)
    root.mainloop()


if __name__ == '__main__':
    main()

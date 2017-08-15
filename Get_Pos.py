# -*- coding:utf-8 -*-
import csv
from tkinter import *
import tkFileDialog
import os

dic_pos = {}
flag = 0
temp_name = ''


def output_csv():
    global dic_pos
    global output_file
    with open(output_file, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Path','X','Y','Altitude','Omega','Phi','Kappa'])
        for x in dic_pos:
            csvWriter.writerow([x, dic_pos[x][0], dic_pos[x][1], dic_pos[x][2], dic_pos[x][3], dic_pos[x][4], dic_pos[x][5]])
        csvFile.close()


def get_info(info_type, line):
    line = line.strip('\r\n').replace('\'', '').replace('\"', '')
    if info_type == 'name':
        return line[9:]
    elif info_type == 'coordinate':
        coordinate = float(line[34:].split(' ')[0]) + float(line[34:].split(' ')[2]) / 60 + float(
            line[34:].split(' ')[3]) / 3600
        if line[-1] in ('W','S'):
            return '-' + str(coordinate)
        else:
            return str(coordinate)
    elif info_type == 'alt':
        return line[34:].split(' ')[0]
    elif info_type == 'angle':
        if '0.00' in line:
            return '0'
        elif '+' in line:
            return line[34:].replace('+', '')
        else:
            return line[34:]


def getpos(path):
    global flag
    global dic_pos
    global temp_name
    command = r'exiftool -GPSLongitude -GPSLatitude -GPSAltitude -CameraRoll -CameraPitch -CameraYaw  ' + path  # 可以直接在命令行中执行的命令
    r = os.popen(command)  # 执行该命令
    info = r.readlines()  # 读取命令行的输出到一个list
    count = len(info)
    for index, item in enumerate(info):
        if index == count - 2:
            break
        elif index % 7 == 0:
            flag = index
            pic_name = get_info('name', item)
            temp_name = pic_name
            dic_pos[pic_name] = []
            # print pic_name
        elif index < flag + 3:
            coordinate = get_info('coordinate', item)
            dic_pos[temp_name].append(coordinate)
            # print coordinate
        elif index == flag + 3:
            alt = get_info('alt', item)
            dic_pos[temp_name].append(alt)
            # print alt
        elif index > flag + 3:
            angle = get_info('angle', item)
            dic_pos[temp_name].append(angle)
            # print angle
    output_csv()


def selectPath():
    global dic_pos
    global output_file
    dic_pos = {}
    path_ = tkFileDialog.askdirectory(parent=root, initialdir="/", title='选择照片路径')
    if path_=='':
        return 0
    path.set(path_)
    output_file = tkFileDialog.asksaveasfilename(filetypes=[('CSV file', '.csv'), ('All files', '*')],
                                                 title='请选择结果存放位置', defaultextension='.csv')
    if os.path.isfile(output_file):
        os.remove(output_file)
    getpos(path_)
    os.system(output_file.decode('utf-8').encode('MBCS'))


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


def main():
    global root
    global path_
    global path
    root = Tk()
    root.title('EXIF_POS提取工具(DJI版)')
    center_window(root, 330, 35)
    path = StringVar()
    Label(root, text="目标路径:").grid(row=0, column=0)
    Entry(root, textvariable=path).grid(row=0, column=1)
    Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)
    root.mainloop()


if __name__ == '__main__':
    main()

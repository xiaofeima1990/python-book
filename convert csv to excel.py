#coding:utf-8

import pandas as pd
import numpy as np
import jieba
import sys 
import os
import glob
import codecs
import csv

# csv.field_size_limit(sys.maxsize)

reload(sys)  
sys.setdefaultencoding('utf8')

###################################
# This is a program aiming to convert csv file into excel file 
# which helps simplify read and write process
# environment is python2.7 
###################################


print "created by xiaofeima, environment is python27"

savefile=[]
path = "F:\\DATAbase\\land\\fm_land\\"
# read_file_list =os.listdir(path)

read_file_list = glob.glob(path+'*.csv')
read_file_list
savefile=[]
for element in read_file_list:
    savefile.append(os.path.splitext(os.path.basename(element)))
    

from xlsxwriter.workbook import Workbook

new_path="F:\\DATAbase\\land\\fm_land\\data\\"


for csvfile in savefile:
    print csvfile
    workbook = Workbook(new_path+csvfile[0] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with codecs.open(path+csvfile[0]+csvfile[1], 'rb',encoding='utf-8-sig',errors='ignore') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col.decode('utf-8','ignore'))
    workbook.close()

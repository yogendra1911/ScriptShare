############################################################
# Create an attedance list with MS teams meeting attendance#
# csv files.                                               #
# V0.2 - muster generation                                 #
# V0.3 - bugfix duplicate entry of faculty                 #
# V0.4 - percentage attendace of students                  #
#        auto musterfile generation                        #
# V0.5 - Date extraction from file, no need to rename the  # 
#        original attendance files                         #
# Run as:                                                  #
# `$ python attendance.py`                                 #
# Author - Yogendra Tank                                   #
############################################################

import os
from datetime import datetime
# def removeEmpty(l):
#     for i in range(len(l)):
#         l[i]=l[i].strip()
#     return list(filter(None,l))
      
students = {}
attendance2 = {}
datesMaster = []

for file in os.listdir("./"):
    att_for_date = []
    att = {}
    att_date = ''
    if file.endswith(".csv"):
        f = open(file,encoding="utf-16")
        lines = f.readlines()
        #lines = removeEmpty(lines)
        enroll = []
        for i in range(3,len(lines)):
                if lines[i] == '\x00': continue
                if "-" not in lines[i]: continue #escape duplicate entry for faculty name
                l = str(lines[i].split("\t")[2].strip('"').strip()) ## Read the datetime from the line
                tmp = datetime.strptime(l.split("\t")[-1],'%m/%d/%Y, %H:%M:%S %p') 
                tempDate = tmp.strftime("%d %b %Y")
                if tempDate not in datesMaster:
                    datesMaster.append(tempDate)
                a = lines[i].split("\t")[0].split("-")
                name = a[-1]
                enroll = a[-2]
                students[enroll] = name
                att[enroll] = tempDate  
                att_date = tempDate	
        f.close()
    for k in att:
        att_for_date.append(k) 
    attendance2[att_date] = att_for_date

f = open("./temp","w")     
f.write("Enrollment Number , Student Name,")
for date in datesMaster:
    f.write(date+",")
f.write("% \n")
for studs in students:
    p=0
    dt = 0
    f.write (str(studs)+","+str(students[studs])+",")
    for date in datesMaster:
        dt = dt+1
        if studs in attendance2[date]:
            f.write("P,")
            p = p+1
        else:
            f.write("A,")
    f.write(str(round((p*100)/dt,2))+"\n")
f.close()
os.rename("./temp","Att-Muster.csv")

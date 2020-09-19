############################################################
# Create an attedance list with MS teams meeting attendance#
# csv files. The files needs to be renamed to have date as #
# last part of the filename - ex. "att - aug 05.csv"       #
# Redirect output to a file to store the result and rename #
# as CSV                                                   #
# V0.2 - muster generation                                 #
# V0.3 - bugfix duplicate entry of faculty                 #
# Run as:                                                  #
# `$ python attendance.py > musterFile`                    #
# Author - Yogendra Tank                                   #
############################################################

import os 
def removeEmpty(l):
    for i in range(len(l)):
        l[i]=l[i].strip()
    return list(filter(None,l))

def extract_dates():
    dates = []
    for file in os.listdir("./"):
        if file.endswith(".csv"):
            dates.append(" ".join(file.split(".")[0].split(" ")[-2:]))
    return dates         

dt = ''
students = {}
attendance2 = {}
dates = extract_dates()

for file in os.listdir("./"):
    att_for_date = []
    att = {}
    att_date = ''
    if file.endswith(".csv"):
        dt = " ".join(file.split(".")[0].split(" ")[-2:])
        f = open(file)
        lines = f.readlines()
        lines = removeEmpty(lines)
        enroll = []
        for i in range(3,len(lines)):
                if lines[i] == '\x00': continue
                if "-" not in lines[i]: continue #escape duplicate entry for faculty name
                a = lines[i].split("\t")[0].split("-")
                name = a[-1]
                enroll = a[-2]
                students[enroll] = name
                att[enroll] = dt  
                att_date = dt
    for k in att:
        att_for_date.append(k)
    attendance2[att_date] = att_for_date    
print("Enrollment Number\tStudent Name",end="\t")
for date in dates:
    print(date,end="\t")
print()
for studs in students:
    print (studs+"\t"+students[studs],end="\t")
    for date in dates:
        if studs in attendance2[date]:
            print("P",end="\t")
        else:
            print("A",end="\t")
    print()

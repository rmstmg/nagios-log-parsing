#!/usr/bin/python
import os
import sys
import re
import glob
import operator
from collections import OrderedDict
from datetime import datetime

f = open( 'nagiosdata', 'w')
#path ="/root/nagios/log/"
#dirs = os.listdir( path )
#for file in dirs:
#nagioslog = open('nagios-06-08-2015-00.log')
nagioslog = open('/root/nagios/log/nagios-' + datetime.now().strftime("%m-%d-%Y") + '-00.log')
#    nagioslog = open('nagios-' + datetime.now().strftime("%m-%d-%Y") + '-00.log')
for line in nagioslog:
    line = line.rstrip()
    if re.search('DOWN;SOFT;3;', line) :
        f.write(line+'\n')
    if re.search('DOWN;HARD;10;CRITICAL', line) :
        f.write(line+'\n')

od = OrderedDict()

with open('nagiosdata') as f:
    r = re.compile("(?<=HOST ALERT:\s)\S+")
    for line in f:
        name, st, con, _, _ = r.search(line).group().split(";")
#        od.setdefault(name, {"State": st, "Total": con,"HARD": 0,"SOFT":0,"Count":0,})
        od.setdefault(name, {"State": st, "HARD": 0,"SOFT":0,"Count":0})
        od[name]["State"] = st
#        od[name]["Total"] = con
        od[name]["Count"] += 1
        if con == 'HARD' :
            od[name]["HARD"] +=1
        else :
            od[name]["SOFT"] +=1
print "Host Down Statistics for last 24 hours: \n"
for k,v in sorted(od.items(), key=operator.itemgetter(1),reverse=True):
    print("{0} {1} ".format(k,v))

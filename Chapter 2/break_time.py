#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 12:32:29 2017

@author: denniswang
"""
import webbrowser
import time

url = ["www.baidu.com","www.sina.com.cn","www.youku.com"]
new = 2

wb = webbrowser.get('Safari')

total_break = 3
break_count = 0

print "The Program is starting at " + time.ctime()
while break_count < total_break:
    time.sleep(10)
    wb.open(url[break_count],new=2)
    break_count += 1
    
print "The Progream stopped at " + time.ctime()

#while break_count < break_count:
#    
#    wb.open(url,new)
#    break_count += 1

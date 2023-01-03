# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:41:17 2019

@author: Scott
"""

in_file = 'E:\Music\Playlists\Test.m3u'
out_file = 'E:\Music\Playlists\Mobile\Test.m3u8'

f = open(in_file,"r")
g = open(out_file,"w")

for line in f:
    x = line.split('\\')
    strt = line.find(x[3])
    print(line[strt:])
    g.write(line[strt:])
    
f.close()
g.close()
    
    

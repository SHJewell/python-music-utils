# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:41:17 2019

@author: Scott
"""

in_file = 'E:\Music\Playlists\Test.m3u'
out_file = 'E:\Documents\Coding\Playlist Functions\Test.m3u8'

f = open(in_file,"r")

for line in f:
    x = line.split('\\')
    print(x[3:])
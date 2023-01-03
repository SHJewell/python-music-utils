# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:40:48 2019

@author: Scott
"""

import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

filename = askopenfilename(title="Select main playlist folder (save new playlists there)")
o_path = os.path.dirname(filename)

dirs = os.listdir(o_path)

for file in dirs:
    if 'Test' in file:
        continue
    if 'Library' in file:
        continue
    if 'Civ' in file:
        continue
    if '.m3u' in file:
        print(file)
        
        out_file = f'{o_path}/Mobile/{file[:-4]}.m3u8'
        #print(out_file)
        
        o_file = f'{o_path}/{file}'
        f = open(o_file, "r")
        g = open(out_file, "w")
        
        g.write('#\n')
        
        for line in f:
            x = line.split('/')
            strt = line.find(x[3])
            g.write(line[strt:])
        
        f.close()
        g.close()
        
Tk().withdraw()

print("Playlists written to", o_path + '/Mobile')
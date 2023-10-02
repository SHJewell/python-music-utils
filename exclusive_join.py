# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 13:34:26 2020

@author: Scott
"""

import os
#from tkinter import Tk
#from tkinter.filedialog import askopenfilename

new_path = "E:\Music\Playlists\Joined"

def get_tracks(file,depth):
    
    tracks = set()
    
    with open(file,"r") as f:
        
        for line in f:
            x = line.split('\\')
            temp = ""
            
            for n in range(depth,len(x)):
                temp += x[n] + "\\"
                
            tracks.add(temp)
        
    return tracks
        
def write_playlist(tracks,name):
    
    path = "E:\Music\Albums\\"
    with open(name,"w") as f:
        
        for elem in tracks:
            
            f.write(path + elem[:-1])
    
        

# filename = askopenfilename(title="Select main playlist folder")
# path1 = os.path.dirname(filename)
path1 = "E:\Music\Playlists\All.m3u"

contents1 = os.listdir(path1)

# filename = askopenfilename(title="Select main playlist folder")
# path2 = os.path.dirname(filename)
path2 = "E:\Music\Playlists\Laptop"

contents2 = os.listdir(path2)

for file in contents1:

    if ".m3u" not in file:
        continue
    
    track_list1 = get_tracks(path1 + "\\" + file,3)
    
    if file in contents2:
        track_list2 = get_tracks(path2 + "\\" +  file,5)
        contents2.remove(file)
        
    joined_list = track_list1.union(track_list2)
    
    write_playlist(joined_list,new_path + "\\" +  file)
    
for file in contents2:
    
    track_list = get_tracks(path2 + "\\" + file,5)    
    write_playlist(track_list,new_path + "\\" +  file)


# for file in dirs:
#     if 'Test' in file:
#         continue
#     if 'Library' in file:
#         continue
#     if 'Civ' in file:
#         continue
#     if '.m3u' in file:
#         print(file)
        
#         out_file = o_path + '/Mobile/' + file[:-4] + '.m3u8'
#         #rint(out_file)
        
#         o_file = o_path + '//' + file
#         f = open(o_file,"r")
#         g = open(out_file,"w")
        
#         g.write('#\n')
        
#         for line in f:
#             x = line.split('\\')
#             strt = line.find(x[3])
#             g.write(line[strt:])
        
#         f.close()
#         g.close()
        
#Tk().withdraw()

# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:40:48 2019

@author: Scott
"""

import os
import io

def repath_playlists(music_lib: str, read_path: str, export_path: str, ext: str):

    # filename = askopenfilename(title="Select main playlist folder (save new playlists there)")
    # o_path = pfd.select_folder('').result()
    # o_path = os.path.dirname(filename)

    #dirs = os.listdir(o_path)

    for file in os.listdir(read_path):
        if 'Test' in file:
            continue
        if '.m3u' in file:
            print(file)

            out_file_path = f'{export_path}/{file[:-4]}{ext}'
            #print(out_file)

            open_file = f'{playlist_path}{file}'
            with io.open(open_file, errors='ignore') as f:
                with open(out_file_path, "w") as g:

                    if ext == '.m3u8':
                        g.write('#\n')

                    for line in f:

                        line = line.replace('\n', '')
                        line = line.replace('\r', '')
                        album = f'{line[line.find("Albums") + len("Albums") + 1:]}\n'

                        if '/' not in line:
                            album = album.replace('\\', os.sep)

                        g.write(f'{music_lib}{album}')

            f.close()


if __name__ == "__main__":
    music_lib = f'/media/disc1/Music/Albums/'
    playlist_path = f'/media/disc1/Music/Playlists (copy)/'
    export_path = f'/home/shjewell/Music/Playlists'
    pl_ext = '.m3u'

    repath_playlists(music_lib, playlist_path, export_path, pl_ext)
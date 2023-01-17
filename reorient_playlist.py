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
        ext_l = 4

        if 'Test' in file:
            continue

        if '.m3u' == file[-4:]:
            ext_l = 4
        elif '.m3u8' == file[-5:]:
            ext_l = 5
        else:
            continue

        print(file)

        out_file_path = f'{export_path}/{file[:-ext_l]}{ext}'

        open_file = f'{playlist_path}{file}'
        with io.open(open_file, errors='ignore') as f:
            with open(out_file_path, "w") as g:

                if ext == '.m3u8':
                    g.write('#\n')

                for line in f:

                    if '/' not in line and '\\' not in line:
                        continue

                    line = line.replace('\n', '')
                    line = line.replace('\r', '')
                    if line.count('\\') > 2 or line.count('/') > 2:
                        album = f'{line[line.find("Albums") + len("Albums") + 1:]}\n'
                    else:
                        album = line + '\n'

                    if '/' not in line:
                        album = album.replace('\\', os.sep)

                    g.write(f'{music_lib}{album}')

        f.close()


if __name__ == "__main__":
    music_lib = f'/media/disc1/Music/Albums/'
    playlist_path = f'/home/shjewell/Music/Mobile Playlists/'
    export_path = f'/home/shjewell/Music/New/'
    pl_ext = '.m3u'

    repath_playlists(music_lib, playlist_path, export_path, pl_ext)
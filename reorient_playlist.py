# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:40:48 2019

@author: Scott
"""

import os
import io
import sys
import yaml

class playlistObj:
    def __init__(self, config_path):
        self.config_path = config_path
        self.divider = "//"
        if sys.platform == "win32":
            self.divider = "\\"

        self.importConfig()

    def importConfig(self):

        with open(self.config_path, "r") as stream:
            config = yaml.safe_load(stream)

        paths = config["paths"]

        self.new_path = paths["new"]
        self.old_path = paths["old"]
        self.extension = config["extension"]

        if "lib" in paths:
            self.library_path = paths["lib"]



    def repathPlaylist(self):

        #dirs = os.listdir(o_path)

        for file in os.listdir(self.old_path):
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

            out_file_path = f'{self.new_path}/{file[:-ext_l]}{self.extension}'

            open_file = f'{self.old_path}{file}'
            with io.open(open_file, errors='ignore') as f:
                with open(out_file_path, "w") as g:

                    if self.extension == '.m3u8':
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

                        g.write(f'{self.library_path}{album}')

            f.close()


if __name__ == "__main__":
    config = "reorient_config.yml"

    playlist = playlistObj(config)
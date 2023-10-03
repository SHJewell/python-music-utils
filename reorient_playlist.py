# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:40:48 2019

@author: Scott
"""

import os
import io
import sys
import yaml
import logging
import re

class playlistObj:
    def __init__(self, path, ext):
        self.path = path
        self.extension = ext
        self.raw_content = []
        self.obj_paths = []
        self.music_file_objs = {}
        self.updated_content = []

        self.sys_divider = "//"
        if sys.platform == "win32":
            self.sys_divider = "\\"


    def readPlaylist(self):

        current_Obj = "header"

        with open(self.path, "r") as original:
            for line_number, line in enumerate(original, start=1):
                line = line.strip()  # Remove leading/trailing whitespace and newline characters
                self.raw_content.append(line)
                if self.sys_divider in line:
                    current_Obj = line
                    self.obj_paths.append(line)

                self.music_file_objs.setdefault(current_Obj, []).append(line)  #appends to list whether it exists or not


    def _repath_m3u(self):

        for media_file in self.obj_paths:
            line = media_file.replace('\n', '')
            line = line.replace('\r', '')
            self.updated_content.append(line.replace(self.orig_path, self.new_path))


    def _repath_m3u8(self):
        """
        TODO:
            Add in m3u8 EXT stuff...?

        """

        self.updated_content = ["#"]

        for line in self.raw_content:
            if self.sys_divider in line:
                line = line.replace('\n', '')
                line = line.replace('\r', '')
                self.updated_content.append(line.replace(self.orig_path, self.new_path))
            elif line == "#":
                continue
            else:
                self.updated_content.append(line)


    def repathPlaylist(self, orig_path, new_path):
        self.orig_path = orig_path
        self.new_path = new_path

        if self.extension == "m3u":
            self._repath_m3u()
        if self.extension == "m3u8":
            self._repath_m3u8()

        return self.updated_content


class playlistCollection:
    def __init__(self, config_path):
        self.config_path = config_path
        self.repath_flag = True
        self.read_ext = "m3u"
        self.sys_divider = "//"
        if sys.platform == "win32":
            self.sys_divider = "\\"
        self.skip_list = []

        self.importConfig()

    def importConfig(self):

        with open(self.config_path, "r") as stream:
            config = yaml.safe_load(stream)

        paths = config["paths"]

        self.new_path = paths["new"]
        self.old_path = paths["old"]
        self.extension = config["extension"]

        if "old_lib" in paths:
            self.old_library_path = paths["old_lib"]

        if "new_lib" in paths:
            self.old_library_path = paths["new_lib"]
            self.repath_flag = True

        self.skip_list = [item.lower() for item in config["meta"]["skip"]]

        self.target_divider = config["meta"]["export delim"]


    def repathCollection(self):

        collection = os.listdir(self.old_path)

        for file in os.listdir(collection):

            if any(item in file for item in self.skip):
                continue

            if '.m3u' == os.path.splittext(file)[-1]:
                self.read_ext = "m3u"
            elif '.m3u8' == os.path.splittext(file)[-1]:
                self.read_ext = "m3u8"
            else:
                continue

            playlist = playlistObj(file, self.read_ext)
            playlist.readPlaylist()
            new_playlist = playlist.repathPlaylist(self.old_path, self.new_path)

            with open()




if __name__ == "__main__":
    config = "reorient_config.yml"

    playlist = playlistCollection(config)

    # playlist = playlistObj("E:\\Music\\Playlists\\From Mobile\\New.m3u8", "m3u8")
    # playlist.readPlaylist()
    # print(playlist.path)
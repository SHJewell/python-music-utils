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

logging.basicConfig(level=logging.DEBUG)

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

    def _repathLine(self, line):
        line = line.strip()

        if self.orig_path is None:
            self.updated_content.append(os.path.join(self.new_path, line))
        elif self.new_path is None:
            self.updated_content.append(line.replace(self.orig_path, ""))
        else:
            self.updated_content.append(line.replace(self.orig_path, self.new_path))


    def _repath_m3u(self):

        for media_file in self.obj_paths:
            self._repathLine(media_file)

    def _repath_m3u8(self):
        """
        TODO:
            Add in m3u8 EXT stuff...?

        """

        self.updated_content = ["#"]

        for line in self.raw_content:
            if self.sys_divider in line:
                self._repathLine(line)
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
        self.read_ext = "m3u"
        self.sys_divider = "//"
        if sys.platform == "win32":
            self.sys_divider = "\\"
        self.skip_list = []

        self.importConfig()

    def importConfig(self):

        logging.debug("Importing config %s" % self.config_path)

        with open(self.config_path, "r") as stream:
            config = yaml.safe_load(stream)

        paths = config["paths"]

        self.old_path = paths["read"]
        self.new_path = paths["export"]
        self.extension = config["extension"]

        logging.debug("Will convert %s playists to %s as %s" % (self.old_path, self.new_path, self.extension))

        self.old_library_path = paths["old_lib"]
        self.new_library_path = paths["new_lib"]

        logging.debug("Will change %s library to %s" % (self.old_library_path, self.new_library_path))

        self.skip_list = [item.lower() for item in config["meta"]["skip"]]

        logging.debug("Will skip playlists containing the following words:")

        for item in self.skip_list:
            logging.debug("     %s" % item)

        self.target_divider = config["meta"]["export delim"]


    def repathCollection(self):

        for file in os.listdir(self.old_path):

            if any(item in file for item in self.skip_list):
                continue

            if '.m3u' == os.path.splitext(file)[-1]:
                self.read_ext = "m3u"
            elif '.m3u8' == os.path.splitext(file)[-1]:
                self.read_ext = "m3u8"
            else:
                continue

            logging.info("Converting %s" % file)

            playlist = playlistObj(os.path.join(self.old_path, file), self.extension["export"])
             playlist.readPlaylist()
            new_playlist = playlist.repathPlaylist(self.old_library_path, self.new_library_path)

            new_file_name = os.path.join(self.new_path, f"{os.path.splitext(file)[0]}.{self.extension['export']}")

            logging.debug("Writing file to %s" % new_file_name)

            with open(new_file_name, "w") as new_file:
                for line in new_playlist:
                    new_file.write(line)
                    new_file.write("\n")


if __name__ == "__main__":

    config = "reorient_config.yml"

    playlist = playlistCollection(config)
    playlist.repathCollection()

    # playlist = playlistObj("E:\\Music\\Playlists\\From Mobile\\New.m3u8", "m3u8")
    # playlist.readPlaylist()
    # print(playlist.path)
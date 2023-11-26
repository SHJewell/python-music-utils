import os
import re


def normalize_name(file_name):
    # Remove numeric characters and any other non-alphabetic characters
    alpha = re.sub('[^a-zA-Z]', '', file_name)
    if not alpha:
        return file_name
    return alpha


class musicLibrary:

    def __init__(self, path: str):
        self.basePath = path
        self.raw_lib = dict
        self.possible_duplicates = dict
        self.short_rounds = dict


    def crawlLib(self):

        for root, dirs, files in os.walk(self.path):

            if not files:
                continue

            self._findMP3s(root, files)


    def _findMP3s(self, root, files):

        for file in files:

            if ".mp3" in file:
                self.raw_lib[f"{root}"]


if __name__ == "__main__":

    #my_library = musicLibrary("E:\\Music\\Albums")
    for root, dirs, files in os.walk("E:\Music\Albums"):
        print(root, dirs)
        for file in files:
            print(file)

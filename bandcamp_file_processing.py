import os
import logging
import zipfile
import shutil

logging.basicConfig(level=logging.DEBUG)

class bandcampRawZip:
    def __init__(self, path: str, library: str):
        self.zip_path = path
        self.lib_path = library
        self.new_folder: str


    def extract_zip(self):
        """
        Extract files from a .zip archive.

        Parameters:
        - zip_path: Path to the .zip file
        - output_folder: Folder where extracted files will be saved
        """

        logging.debug("Extracting %s to temporary file" % self.zip_path)

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall("temp")


    def create_album_folder(self):

        filename = os.path.basename(os.path.splitext(self.zip_path)[-2])
        artist = filename.split(" - ")[0]
        album = filename.split(" - ")[1]

        # library = os.listdir(self.lib_path)
        self.new_folder = os.path.join(self.lib_path, artist, album)

        logging.debug("Creating new folder %s" % self.new_folder)

        try:
            os.makedirs(self.new_folder)
        except FileExistsError:
            pass


    def copy_and_rename(self):

        logging.debug("Copying files...")

        for item in os.listdir("temp"):

            if os.path.splitext(item)[-1] in [".jpg", ".png"]:
                shutil.copy2(os.path.join("temp", item), os.path.join(self.new_folder, item))

                logging.debug("Copying %s to %s" % (item, os.path.join(self.new_folder, item)))

            elif os.path.splitext(item)[-1] == ".mp3":
                """
                Making a somewhat dangerous assumption here that I can use " - " as my delimiter. It may not work in all
                cases. So, should this be put into a config?
                """

                first_delim = item.find(" - ")
                second_delim = item.find(" - ", first_delim + 1)

                name = item[second_delim+6:]
                #os.rename()

                shutil.copy2(os.path.join("temp", item), os.path.join(self.new_folder, name))

                logging.debug("Copying %s to %s" % (item, os.path.join(self.new_folder, name)))

    def cleanup(self):

        shutil.rmtree("temp")
        logging.debug("Removing temporary folder")


    def processNewMusic(self):
        self.extract_zip()
        self.create_album_folder()
        self.copy_and_rename()
        self.cleanup()


def collect_zips(path):

    files = []

    for file in os.listdir(path):
        if file.endswith("zip"):
            files.append(f"{path}\\{file}")

    return files

def batchProcess(path, library):

    for file in collect_zips(path):
        bcfolder = bandcampRawZip(file, library)
        bcfolder.processNewMusic()



if __name__ == "__main__":

    batchProcess(r"E:\Music\Raw Compressed", r"E:\Music\Albums")
    # bcfolder = bandcampRawZip(r"E:\Music\Raw Compressed\Andrew Bird - Sunday Morning Put-On.zip",
    #                           "E:\\Music\\Albums\\")
    # bcfolder.processNewMusic()
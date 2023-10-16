import os
import logging
import zipfile

logging.basicConfig(level=logging.DEBUG)

class bandcampRawZip:
    def __init__(self, path, library):
        self.zip_path = path
        self.lib_path = library


    def extract_zip(self, zip_path, output_folder):
        """
        Extract files from a .zip archive.

        Parameters:
        - zip_path: Path to the .zip file
        - output_folder: Folder where extracted files will be saved
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
            logging.info("Files extracted to: " % output_folder)


    def create_album_folder(self):

        filename = os.path.splitext(self.zip_path)[-2]
        artist = filename.split(" - ")[0]
        album = filename.split(" - ")[1]

        library = os.listdir(self.lib_path)

        os.makedirs(os.path.join(library, artist, album))





def collect_zips(path):

    files = []

    for file in os.listdir(path):
        if os.path.splitext(file)[-1] == "zip":
            files.append(file)



if __name__ == "__main__":

    bandcamp(
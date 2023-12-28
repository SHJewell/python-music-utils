import os
import re
from mutagen.mp3 import MP3
from mutagen.wavpack import WavPack
from mutagen.oggvorbis import OggVorbis
from mutagen import File
import os
import yaml
import logging


def normalize_name(file_name):
    # Remove numeric characters and any other non-alphabetic characters
    alpha = re.sub('[^a-zA-Z]', '', file_name)
    if not alpha:
        return file_name
    return alpha


class musicLibrary:

    def __init__(self, path: str):
        self.basePath = path
        self.raw_lib = dict()
        self.possible_duplicates = dict()
        self.short_rounds = dict()


    def _findMP3s(self, root, files):

        for file in files:

            if ".mp3" in file:
                self.raw_lib[f"{root}"]


    def get_metadata(self, file_path):
        """
        TODO:
            Log error messages caught by try-except
        """

        switch = {"artist": ['TPE1', 'ARTIST'],
                  "album":  ['TALB', 'ALBUM'],
                  "title":  ['TIT2', 'TITLE']}

        file_extension = os.path.splitext(file_path)[1].lower()

        # Load the file based on its type
        try:
            if file_extension == '.mp3':
                audio = MP3(file_path)
            elif file_extension == '.wav':
                audio = WavPack(file_path)
            elif file_extension == '.ogg':
                audio = OggVorbis(file_path)
            else:
                return False
        except Exception as e:
            logger.error("Bad extraction in %s", file_path, exc_info=e)
            return {
                "Artist": "",
                "Album": "",
                "Title": "",
                "Length (seconds)": "",
                "Format": file_extension,
                "Path": file_path
            }

        aat = []

        # Extracting metadata
        for n, attr in enumerate(["artist", "album", "title"]):

            try:
                aat.append(audio.get(switch.get(attr)[0], "Unknown Artist").text[0] if file_extension == ".mp3" else \
                    audio.get(switch.get(attr)[1], ["Unknown Artist"])[0])
            except AttributeError as e:
                logger.error("Bad extraction in %s", file_path)
                logger.error("Trying without casting to string")
                logging.error("%s", exc_info=e)
                aat.append(audio.get(switch.get(attr)[0], "Unknown Artist")[0] if file_extension == ".mp3" else \
                    audio.get(switch.get(attr)[1], ["Unknown Artist"])[0])

        length = str(int(audio.info.length))  # Length in seconds

        return {
            "Artist": aat[0],
            "Album": aat[1],
            "Title": aat[2],
            "Length (seconds)": length,
            "Format": file_extension,
            "Path": file_path
        }

    def genNewLib(self):

        idno = 0

        for root, dirs, files in os.walk(self.basePath):

            if not files:
                continue

            logger.info(root)

            for file in files:
                meta = self.get_metadata(os.path.join(root, file))

                if meta:
                    meta["Path"] = os.path.join(root, file)

                    self.raw_lib[str(idno).zfill(6)] = meta
                    idno += 1

        with open("master_lib.yml", "w") as yml:
            yaml.dump(self.raw_lib, yml)




if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('create_library_error.log')
    file_handler.setLevel(logging.ERROR)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    mylib = musicLibrary(r"E:\Music\Albums")
    mylib.genNewLib()

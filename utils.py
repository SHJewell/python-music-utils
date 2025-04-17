import os

def remove_duplicates(path, write_path):

    with open(path, 'r') as file:
        lines = file.readlines()

    no_dupes = set(lines)

    with open(write_path, 'w') as file:
        for line in no_dupes:
            file.write(line)

def check_for_archive_path(path):

    album_path = r"E:\Music\Albums"
    archive_path = r"E:\Music\Raw Compressed"
    amazon_path = r"E:\Music\Amazon Music"

    if path.startswith(amazon_path):
        return False
    elif path.startswith(archive_path):
        return False

    return path

def check_playlist(playlist_path):

    flags = []

    with open(playlist_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if not check_for_archive_path(line):
            flags.append(line)

    return flags

def cycle_playlists(folder):

    for file in os.listdir(folder):

        if ".m3u" not in file:
            continue
        temp = check_playlist(os.path.join(folder, file))

        if temp != []:
            print(file)
            print(temp)

    return


if __name__ == "__main__":

    cycle_playlists(r"E:\Music\Playlists")
    # remove_duplicates("E:\Music\Playlists\All.m3u", "test.m3u")
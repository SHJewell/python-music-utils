import os


def m3u_reorient(read_path, old_music_path, new_music_path):

    new_file = []

    with open(read_path, 'r', encoding='utf-8', errors='replace') as m3u_file:

        for line in m3u_file:
            line = line.strip()

            line = line.replace(old_music_path, new_music_path)

            normalized_path = os.path.normpath(line)
            new_file.append(normalized_path)

    return new_file

def write_new_m3u(new_file, write_path):

    with open(write_path, 'w', encoding='utf-8') as m3u_file:
        for line in new_file:
            m3u_file.write(line + "\n")

    return

def main():

    lib_path = r"E:\Music\Playlists"
    old_music_path = r"E:\Music\Albums"
    new_music_path = r"MUSIC"
    write_path = r"I:\PLAYLISTS"

    for file in os.listdir(lib_path):
        if file.endswith(".m3u"):
            print(f"Processing {file}")
            new_playlist = m3u_reorient(os.path.join(lib_path, file), old_music_path, new_music_path)
            write_new_m3u(new_playlist, os.path.join(write_path, file))
            print(f"Writing to {os.path.join(write_path, file)}")

    return

if __name__ == "__main__":
    main()

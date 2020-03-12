from pathlib import Path

from server.logic.song import Song

random_url = "https://www.lyrics.com/random.php"


def persist_random_collection(dir_path: Path, n: int = 100):
    counter = 0
    urls = set()
    while counter < n:
        song = Song(random_url, dir_path)
        if song.url in urls:
            continue
        try:
            song.get()
            song.parse()
        except:
            song.remove()
            continue
        urls.add(song.url)
        counter += 1
        if counter % 50 == 0:
            print(f"Number of crawled songs: {counter}")


def persist_song(url: str, dir_path: Path):
    song = Song(url, dir_path)
    try:
        song.get()
        song.parse()
    except:
        song.remove()
        raise FileNotFoundError


def remove_song(url: str, dir_path: Path):
    song = Song(url, dir_path)
    song.remove()

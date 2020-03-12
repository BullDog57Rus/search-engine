from pathlib import Path
from typing import Set, Dict

from server.logic.song import Song, id_from_url
from server.logic.text_processing import lemmatization_preprocess


class InvertedIndex:

    def __init__(self):
        self.index: Dict[str, Set[str]] = {}
        self.deleted_songs: Set[str] = set()

    def reset(self):
        self.index = {}
        self.deleted_songs = set()

    def add_song(self, song_url: str, song_dir_path: Path):
        song = Song.from_file(id_from_url(song_url), song_dir_path)
        words = lemmatization_preprocess(song.text)
        song_id = id_from_url(song.url)
        self.deleted_songs.discard(song_id)
        for word in words:
            if word not in self.index:
                self.index[word] = {song_id}
            else:
                self.index[word].add(song_id)

    def remove_song(self, song_url):
        self.deleted_songs.add(id_from_url(song_url))

    def get_ids(self, token: str) -> Set[str]:
        return self.index[token] if token in self.index else set()


def persist_index(song_dir_path: Path, index_dir_path: Path):
    counter = 0
    for song_path in song_dir_path.iterdir():
        song = Song.from_file(song_path.name, song_dir_path)
        add_song_to_index(index_dir_path, song)
        counter += 1
        if counter % 50 == 0:
            print(f"Number of indexed songs: {counter}")


def add_song_to_index(index_dir_path: Path, song: Song):
    words = lemmatization_preprocess(song.text)
    song_id = id_from_url(song.url)
    for word in words:
        index_file = index_dir_path / word
        if not index_file.exists():
            with (index_file.open("w")) as file:
                file.write(song_id + "\n")
        else:
            with index_file.open("r+") as file:
                current_song_ids = set(x.strip() for x in file.readlines())
                file.seek(0)
                file.truncate()
                current_song_ids.add(song_id)
                file.write("\n".join(current_song_ids) + "\n")


def update_index(index_dir_path: Path, aux_index: InvertedIndex):
    for (word, song_ids) in aux_index.index.items():
        index_file = index_dir_path / word
        if not index_file.exists():
            with (index_file.open("w")) as file:
                file.write("\n".join(song_ids) + "\n")
        else:
            with index_file.open("r+") as file:
                current_song_ids = set(x.strip() for x in file.readlines())
                file.seek(0)
                file.truncate()
                current_song_ids |= song_ids
                file.write("\n".join(current_song_ids) + "\n")
    for song_path in index_dir_path.iterdir():
        with song_path.open("r+") as file:
            current_song_ids = set(x.strip() for x in file.readlines())
            file.seek(0)
            file.truncate()
            current_song_ids -= aux_index.deleted_songs
            file.write("\n".join(current_song_ids) + "\n")


def get_ids(dir_path: Path, token: str) -> Set[str]:
    assert dir_path.is_dir()
    file_path = dir_path / token
    if file_path.exists() and file_path.is_file():
        with (file_path.open("r")) as file:
            return set(x.strip() for x in file.readlines())
    else:
        return set()

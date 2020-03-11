from pathlib import Path
from typing import Set

from server.logic.song import Song
from server.logic.text_processing import simple_preprocess


def make_dict(song_dir_path: Path) -> Set[str]:
    dictionary = set()
    for song_path in song_dir_path.iterdir():
        song = Song.from_file(song_path.name, song_dir_path)
        words = simple_preprocess(song.text)
        for word in words:
            dictionary.add(word)
    return dictionary

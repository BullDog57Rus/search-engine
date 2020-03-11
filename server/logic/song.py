import base64
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class Song:

    def __init__(self, url: str, dir_path: Path):
        assert dir_path.is_dir()
        self.dir_path = dir_path
        self.url = requests.head(url, allow_redirects=True).url

    @classmethod
    def from_file(cls, file_id: str, dir_path: Path) -> "Song":
        song = Song(url_from_id(file_id), dir_path)
        file_path = dir_path / file_id
        if file_path.exists() and file_path.is_file():
            with (file_path.open("rb")) as file:
                song.content = file.read()
                song.parse()
                return song
        else:
            raise FileNotFoundError(file_path)

    def get(self):
        if not self.load():
            if not self.download():
                raise FileNotFoundError(self.url)
            else:
                self.persist()

    def download(self) -> int:
        r = requests.get(self.url)
        status_ok = r.status_code < 300
        self.content = r.content if status_ok else None
        return status_ok

    def persist(self):
        file_path = self.dir_path / id_from_url(self.url)
        with (file_path.open("wb")) as file:
            file.write(self.content)

    def remove(self):
        file_path = self.dir_path / id_from_url(self.url)
        if file_path.exists() and file_path.is_file():
            file_path.unlink()

    def load(self) -> bool:
        file_path = self.dir_path / id_from_url(self.url)
        if file_path.exists() and file_path.is_file():
            with (file_path.open("rb")) as file:
                self.content = file.read()
            return True
        else:
            return False

    def parse(self):
        soup = BeautifulSoup(self.content, "html.parser")

        self.title = soup.find("h1", {"class": "lyric-title"}).text
        self.artists = [art.text for art in
                        soup.find("h3", {"class": "lyric-artist"})
                            .findAll("a")[:-1]]
        self.text = soup.find("pre", {"class": "lyric-body"}).text


def id_from_url(url: str) -> str:
    return base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8")


def url_from_id(song_id: str) -> str:
    return base64.urlsafe_b64decode(song_id.encode("utf-8")).decode("utf-8")

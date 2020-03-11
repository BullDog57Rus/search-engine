from pathlib import Path

from flask import Flask, request
from flask_api import status

from server.logic.crawler import persist_random_collection, persist_song, \
    remove_song
from server.logic.dictionary import make_dict
from server.logic.inverted_index import persist_index, InvertedIndex, \
    update_index
from server.logic.search import search
from server.logic.soundex_levenshtein import SoundexTree
from server.logic.wildcard_tree import WildCardTree
import json

app = Flask(__name__)

SONGS_PATH = Path("data/songs/")
INDEX_PATH = Path("data/index/")

SONGS_PATH.mkdir(parents=True, exist_ok=True)
INDEX_PATH.mkdir(parents=True, exist_ok=True)

persist_random_collection(SONGS_PATH, 1000)
persist_index(SONGS_PATH, INDEX_PATH)
dictionary = make_dict(SONGS_PATH)
WILDCARD_TREE = WildCardTree(dictionary)
SOUNDEX_TREE = SoundexTree(dictionary)
AUX_INDEX = InvertedIndex()


@app.route('/search')
def search_route():
    query = request.args.get("query")
    return json.dumps(search(query,
                             WILDCARD_TREE,
                             SOUNDEX_TREE,
                             AUX_INDEX,
                             INDEX_PATH,
                             SONGS_PATH))


@app.route('/songs', methods=['POST'])
def add_song():
    song_url = request.args.get("song_url")
    persist_song(song_url, SONGS_PATH)
    AUX_INDEX.add_song(song_url, SONGS_PATH)
    return "", status.HTTP_200_OK


@app.route('/songs', methods=['DELETE'])
def delete_song():
    song_url = request.args.get("song_url")
    remove_song(song_url, SONGS_PATH)
    AUX_INDEX.remove_song(song_url)
    return "", status.HTTP_200_OK


@app.route('/index', methods=["PATCH"])
def patch_index():
    update_index(INDEX_PATH, AUX_INDEX)
    AUX_INDEX.reset()
    return "", status.HTTP_200_OK


if __name__ == '__main__':
    app.run()

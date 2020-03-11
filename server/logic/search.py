from pathlib import Path
from typing import List

from server.logic.inverted_index import get_ids, InvertedIndex
from server.logic.song import Song, url_from_id
from server.logic.soundex_levenshtein import SoundexTree
from server.logic.text_processing import lemmatization_preprocess
from server.logic.wildcard_tree import WildCardTree


def search(query: str,
           wildcard_tree: WildCardTree,
           soundex_tree: SoundexTree,
           aux_index: InvertedIndex,
           index_path: Path,
           song_path: Path) -> List[str]:
    relevant_documents = []
    index_sets = []
    query = lemmatization_preprocess(query)
    for token in query:
        direct_indexes = get_ids(index_path, token) | aux_index.get_ids(token)
        if direct_indexes:
            index_sets.append(direct_indexes)
        else:
            if WildCardTree.asterisk in token:
                found_tokens = wildcard_tree.find_words(token)
            else:
                found_tokens = soundex_tree.find_closest(token)
            common_indexes = set()
            for found_token in found_tokens:
                common_indexes |= (get_ids(index_path, found_token)
                                   | aux_index.get_ids(found_token))
            index_sets.append(common_indexes)
    indexes = set.intersection(*index_sets) if index_sets else set()
    indexes -= aux_index.deleted_songs
    for doc_id in indexes:
        # relevant_documents.append(Song.from_file(doc_id, song_path))
        relevant_documents.append(url_from_id(doc_id))
    return relevant_documents

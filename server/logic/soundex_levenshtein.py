from cmath import inf
from typing import Set, Dict

from jellyfish import soundex, levenshtein_distance


class SoundexTree:

    def __init__(self, dictionary: Set[str]):
        self.soundex_index = self._make_soundex_index(dictionary)

    @classmethod
    def from_dict(cls, tree: Dict[str, Set]) -> "SoundexTree":
        ob = cls(set())
        ob.soundex_index = tree
        return ob

    def to_dict(self) -> Dict[str, Set]:
        return self.soundex_index

    def find_closest(self, found_word: str) -> Set[str]:
        closest_words = set()
        try:
            soundex_words = self.soundex_index[soundex(found_word)]
        except KeyError:
            return closest_words
        min_distance = inf
        for word in soundex_words:
            distance = levenshtein_distance(found_word, word)
            if distance < min_distance:
                min_distance = distance
                closest_words = [word]
            elif distance == min_distance:
                closest_words.append(word)
        return closest_words

    @staticmethod
    def _make_soundex_index(dictionary: Set[str]):
        soundex_index = {}
        for word in dictionary:
            sound = soundex(word)
            if sound not in soundex_index:
                soundex_index[sound] = {word}
            else:
                soundex_index[sound].add(word)
        return soundex_index

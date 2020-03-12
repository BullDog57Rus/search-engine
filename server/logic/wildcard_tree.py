from queue import Queue
from typing import Set, List, Dict


class WildCardTree:
    terminal = "$"
    asterisk = "*"

    def __init__(self, collection: Set[str]):
        counter = 0
        length = len(collection)
        self.root = {}
        for token in collection:
            token = token + self.terminal
            for permuted_token in self._cyclic_permute(token):
                self._add(permuted_token + self.terminal)
            counter += 1
            if counter % (length * 0.1) == 0:
                print(f"WildCard {counter}/{length}")

    @classmethod
    def from_dict(cls, tree: Dict[str, Dict]) -> "WildCardTree":
        ob = cls(set())
        ob.root = tree
        return ob

    def to_dict(self) -> Dict[str, Dict]:
        return self.root

    def find_words(self, wildcard: str) -> Set[str]:
        if wildcard.count(self.asterisk) == 0:
            return self._get_terminal(wildcard)
        if wildcard.count(self.asterisk) != 1:
            return set()
        wildcard = self._cyclic_permute_asterisk(wildcard + self.terminal)
        return {self._cyclic_permute_terminal(word) for word in
                self._get_terminals(wildcard)}

    def _add(self, token: str):
        current_node = self.root
        for key in token:
            if key not in current_node:
                current_node[key] = {}
            current_node = current_node[key]

    def _find_node(self, token):
        current_node = self.root
        for key in token:
            if key not in current_node:
                return None
            current_node = current_node[key]
        return current_node

    def _get_terminal(self, token: str) -> Set[str]:
        current_node = self._find_node(token)
        if self.terminal in current_node:
            return {token}
        else:
            return set()

    def _get_terminals(self, prefix: str) -> List[str]:
        current_node = self._find_node(prefix)
        if not current_node:
            return []
        results = []
        nodes_to_visit = Queue()
        nodes_to_visit.put((current_node, ""))
        while not nodes_to_visit.empty():
            current_node, postfix = nodes_to_visit.get()
            if self.terminal in current_node:
                results.append(prefix + postfix)
            for key in current_node:
                nodes_to_visit.put((current_node[key], postfix + key))
        return results

    @staticmethod
    def _cyclic_permute(word: str):
        for i in range(len(word)):
            yield word[i:] + word[:i]

    @staticmethod
    def _cyclic_permute_terminal(word: str) -> str:
        return next(filter(lambda x: x.endswith(WildCardTree.terminal),
                           WildCardTree._cyclic_permute(word)))[:-1]

    @staticmethod
    def _cyclic_permute_asterisk(word: str) -> str:
        return next(filter(lambda x: x.endswith(WildCardTree.asterisk),
                           WildCardTree._cyclic_permute(word)))[:-1]

# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import override

__all__ = ["TrieNode", "Trie", "WordsTrie", "SentenceTrie"]


class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}  # Store child nodes
        self.is_end_of_word: bool = False  # Marks the end of a word

    # Print the trie structure (depth-first traversal)
    def print(self, word: str, prefix: int, first: bool) -> None:
        if first:
            print(word, end="")
        else:
            print(" " * prefix + word, end="")

        if self.is_end_of_word:
            print("")

        for i, (child, child_node) in enumerate(self.children.items()):
            child_node.print(child, prefix + len(word), i == 0)


class _Trie[Sentence: str | list[str]](abc.ABC):
    def __init__(self, *, case_sensitive: bool = True):
        self._root: TrieNode = TrieNode()
        self._case_sensitive: bool = case_sensitive

    def insert(self, sentence: Sentence) -> None:
        """Insert a sentence into the trie"""
        node = self._root
        for word in self._sentence_to_words(sentence):
            word_key = word if self._case_sensitive else word.lower()
            if word_key not in node.children:
                # Create new node if character doesn't exist
                node.children[word_key] = TrieNode()

            node = node.children[word_key]
        node.is_end_of_word = True  # Mark end of word

    @abc.abstractmethod
    def _sentence_to_words(self, sentence: Sentence) -> list[str]: ...

    def search(self, sentence: Sentence) -> bool:
        """Search for a complete sentence in the trie (case-insensitive)"""
        node = self._root
        for word in self._sentence_to_words(sentence):
            word_key = word if self._case_sensitive else word.lower()
            if word_key not in node.children:
                return False  # Return False if character not found
            node = node.children[word_key]
        return node.is_end_of_word  # Return True if last character marks end of word

    def starts_with(self, prefix: Sentence) -> bool:
        """Check if any sentence in the trie starts with the given prefix"""
        node = self._root
        for word in self._sentence_to_words(prefix):
            word_key = word if self._case_sensitive else word.lower()
            if word_key not in node.children:
                return False  # Return False if character not found
            node = node.children[word_key]
        return True  # Return True if all prefix characters exist

    def print(self) -> None:
        """Print the trie structure (depth-first traversal)"""
        self._root.print("", 0, True)

    def __str__(self) -> str:
        return f"Trie(case_sensitive={self._case_sensitive})"


class Trie(_Trie[str]):
    @override
    def _sentence_to_words(self, sentence: str) -> list[str]:
        return list(sentence)


class WordsTrie(_Trie[list[str]]):
    @override
    def _sentence_to_words(self, sentence: list[str]) -> list[str]:
        return sentence


class SentenceTrie(_Trie[str]):
    def __init__(self, delimiter: str, *, case_sensitive: bool = True):
        super().__init__(case_sensitive=case_sensitive)
        self.delimiter = delimiter

    @override
    def _sentence_to_words(self, sentence: str) -> list[str]:
        return [self.delimiter + word if i != 0 else word for i, word in enumerate(sentence.split(self.delimiter))]

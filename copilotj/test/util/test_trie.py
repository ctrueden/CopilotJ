# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from copilotj.util.trie import SentenceTrie, Trie


@pytest.fixture
def trie():
    t = Trie()
    for word in ["apple", "app", "banana", "bat", "bar", "bark"]:
        t.insert(word)
    return t


def test_insert_and_search(trie):
    # Test existing words
    for word in ["apple", "app", "banana", "bat", "bar", "bark"]:
        assert trie.search(word)

    # Test non-existing words
    assert not trie.search("apples")
    assert not trie.search("ba")
    assert not trie.search("")


def test_starts_with(trie):
    # Test existing prefixes
    assert trie.starts_with("app")
    assert trie.starts_with("ban")
    assert trie.starts_with("bar")

    # Test non-existing prefixes
    assert not trie.starts_with("apx")
    assert not trie.starts_with("baz")
    assert not trie.starts_with("c")


def test_empty_trie():
    empty_trie = Trie()
    assert not empty_trie.search("apple")
    assert not empty_trie.starts_with("a")


def test_partial_words(trie):
    # Test partial words that shouldn't match
    assert not trie.search("appl")
    assert not trie.search("ban")
    assert not trie.search("b")


def test_case_insensitivity():
    trie = Trie(case_sensitive=False)
    trie.insert("Apple")
    assert trie.search("Apple")
    assert trie.search("apple")
    assert trie.search("aPpLe")


@pytest.fixture
def sentence_trie():
    t = SentenceTrie(delimiter=" ")
    for sentence in ["the quick brown fox", "the quick", "the", "quick brown", "brown fox", "fox"]:
        t.insert(sentence)
    return t


def test_sentence_insert_and_search(sentence_trie):
    # Test existing sentences
    for sentence in ["the quick brown fox", "the quick", "the", "quick brown", "brown fox", "fox"]:
        assert sentence_trie.search(sentence)

    # Test non-existing sentences
    assert not sentence_trie.search("the quick brown")
    assert not sentence_trie.search("quick")
    assert not sentence_trie.search("")


def test_sentence_starts_with(sentence_trie):
    # Test existing prefixes
    assert sentence_trie.starts_with("the")
    assert sentence_trie.starts_with("the quick")
    sentence_trie.print()
    assert sentence_trie.starts_with("quick")
    assert sentence_trie.starts_with("brown")

    # Test non-existing prefixes
    assert not sentence_trie.starts_with("thi")
    assert not sentence_trie.starts_with("f")
    assert not sentence_trie.starts_with("abc")


def test_sentence_empty_trie():
    empty_trie = SentenceTrie(delimiter=" ")
    assert not empty_trie.search("the quick brown fox")
    assert not empty_trie.starts_with("the")


def test_sentence_partial_sentences(sentence_trie):
    # Test partial sentences that shouldn't match
    assert not sentence_trie.search("the quick bro")
    assert not sentence_trie.search("bro")
    assert not sentence_trie.search("f")


def test_sentence_case_insensitivity():
    trie = SentenceTrie(delimiter=" ", case_sensitive=False)
    trie.insert("The Quick Brown Fox")
    assert trie.search("The Quick Brown Fox")
    assert trie.search("the quick brown fox")
    assert trie.search("tHe qUiCk bRoWn fOx")

import re
from typing import Set

from bhagavad_gita_api.fallback_verses import DEFAULT_VERSE, FALLBACK_VERSES, VerseCard

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "be",
    "but",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "so",
    "that",
    "the",
    "to",
    "with",
}


def pick_verse(message: str) -> VerseCard:
    tokens = _tokenize(message)
    if not tokens:
        return DEFAULT_VERSE

    best_card = DEFAULT_VERSE
    best_score = -1

    for card in FALLBACK_VERSES:
        score = _score_card(card, tokens)
        if score > best_score:
            best_score = score
            best_card = card

    return best_card


def _score_card(card: VerseCard, tokens: Set[str]) -> int:
    score = 0
    searchable_text = " ".join(card.tags).lower()
    meaning_text = card.meaning.lower()
    advice_text = card.advice.lower()

    for token in tokens:
        if token in searchable_text:
            score += 4
        if token in meaning_text:
            score += 2
        if token in advice_text:
            score += 1

    if {"stress", "pressure", "results"} & tokens and card.reference == "Bhagavad Gita 2.47":
        score += 3
    if {"mind", "focus", "overthinking", "anxiety"} & tokens and card.reference == "Bhagavad Gita 6.26":
        score += 3
    if {"grief", "pain", "loss", "sadness"} & tokens and card.reference == "Bhagavad Gita 2.14":
        score += 3

    return score


def _tokenize(message: str) -> Set[str]:
    words = set(re.findall(r"[a-zA-Z']+", message.lower()))
    return {word for word in words if word not in STOPWORDS and len(word) > 1}

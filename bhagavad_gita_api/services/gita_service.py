import random
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, joinedload

from bhagavad_gita_api.models import gita as models

VEDABASE_BASE = "https://vedabase.io/en/library/bg"

CHAPTER_VERSE_COUNTS = {
    1: 47,
    2: 72,
    3: 43,
    4: 42,
    5: 29,
    6: 47,
    7: 30,
    8: 28,
    9: 34,
    10: 42,
    11: 55,
    12: 20,
    13: 34,
    14: 27,
    15: 20,
    16: 24,
    17: 28,
    18: 78,
}


@dataclass(frozen=True)
class VerseReference:
    chapter: int
    verse: int

    def key(self) -> str:
        return f"{self.chapter}.{self.verse}"


@dataclass(frozen=True)
class VersePayload:
    shloka: str
    translation: str
    word_meaning: str
    source: str


def get_verse(reference: VerseReference, db: Optional[Session] = None) -> VersePayload:
    if db:
        local = _fetch_from_db(reference, db)
        if local:
            return local

    remote = _fetch_from_api(reference)
    if remote:
        return remote

    raise ValueError("Verse not found.")


def random_reference(exclude: Optional[set] = None) -> VerseReference:
    exclude = exclude or set()
    for _ in range(20):
        chapter = random.randint(1, 18)
        verse = random.randint(1, CHAPTER_VERSE_COUNTS[chapter])
        ref = VerseReference(chapter=chapter, verse=verse)
        if ref.key() not in exclude:
            return ref
    return VerseReference(chapter=1, verse=1)


def is_valid_reference(reference: VerseReference) -> bool:
    return (
        1 <= reference.chapter <= 18
        and 1 <= reference.verse <= CHAPTER_VERSE_COUNTS.get(reference.chapter, 0)
    )


def _fetch_from_db(reference: VerseReference, db: Session) -> Optional[VersePayload]:
    try:
        verse = (
            db.query(models.GitaVerse)
            .options(joinedload(models.GitaVerse.translations))
            .filter(
                models.GitaVerse.chapter_number == reference.chapter,
                models.GitaVerse.verse_number == reference.verse,
            )
            .first()
        )
    except OperationalError:
        return None
    if not verse:
        return None

    translation = _pick_translation(verse)
    return VersePayload(
        shloka=verse.text,
        translation=translation or "Translation not available.",
        word_meaning=verse.word_meanings or "",
        source="local-db",
    )


def _pick_translation(verse: models.GitaVerse) -> Optional[str]:
    for author in ("Swami Sivananda", "Shri Purohit Swami", "Dr. S. Sankaranarayan"):
        match = next(
            (t.description for t in verse.translations if t.author_name == author),
            None,
        )
        if match:
            return match
    if verse.translations:
        return verse.translations[0].description
    return None


def _fetch_from_api(reference: VerseReference) -> Optional[VersePayload]:
    url = f"{VEDABASE_BASE}/{reference.chapter}/{reference.verse}/"
    try:
        response = requests.get(
            url,
            timeout=12,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            },
        )
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    return _parse_vedabase_html(response.text)


def _clean_word_meaning(text: str) -> str:
    if not text:
        return ""
    cleaned = text.strip()
    if "Commentary" in cleaned:
        cleaned = cleaned.split("Commentary", 1)[0].strip()
    return cleaned


def _parse_vedabase_html(html: str) -> Optional[VersePayload]:
    soup = BeautifulSoup(html, "html.parser")

    shloka = _extract_section_text(soup, "Devanagari")
    translation = _extract_section_text(soup, "Translation")
    word_meaning = _extract_section_text(soup, "Synonyms")

    if not shloka:
        shloka = _extract_section_text(soup, "Verse text")

    if not shloka and not translation:
        return None

    if not translation:
        translation = "Translation not available."

    return VersePayload(
        shloka=_clean_text_block(shloka),
        translation=_clean_text_block(translation),
        word_meaning=_clean_text_block(word_meaning),
        source="vedabase",
    )


def _extract_section_text(soup: BeautifulSoup, title: str) -> str:
    heading = soup.find(
        lambda tag: tag.name in {"h1", "h2", "h3", "h4"}
        and title.lower() in tag.get_text(" ", strip=True).lower()
    )
    if not heading:
        heading_text = soup.find(string=lambda text: text and title.lower() in text.lower())
        if heading_text:
            heading = heading_text.parent
    if not heading:
        return ""

    parts = []
    for sibling in heading.next_siblings:
        if getattr(sibling, "name", None) in {"h1", "h2", "h3", "h4"}:
            break
        if getattr(sibling, "get_text", None):
            text = sibling.get_text(" ", strip=True)
        else:
            text = str(sibling).strip()
        if text:
            parts.append(text)

    if parts:
        return " ".join(parts).strip()

    paragraph = heading.find_next("p")
    if paragraph:
        return paragraph.get_text(" ", strip=True)

    return ""


def _clean_text_block(text: str) -> str:
    return " ".join(text.split())

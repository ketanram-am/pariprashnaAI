import json
import random
import re
from collections import deque
from typing import Deque, List, Optional

from bhagavad_gita_api.config import settings
from bhagavad_gita_api.services.gita_service import (
    CHAPTER_VERSE_COUNTS,
    VerseReference,
    is_valid_reference,
    random_reference,
)

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

RECENT_VERSES: Deque[str] = deque(maxlen=12)

DIRECT_PATTERNS = [
    re.compile(r"\b(?P<ch>\d{1,2})\s*[.:]\s*(?P<vs>\d{1,3})\b", re.IGNORECASE),
    re.compile(
        r"\bchapter\s*(?P<ch>\d{1,2})\s*(?:verse|sloka|shloka|slok|shlok)\s*(?P<vs>\d{1,3})\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bbg\s*(?P<ch>\d{1,2})\s*[.:]?\s*(?P<vs>\d{1,3})\b", re.IGNORECASE),
    re.compile(
        r"\bgita\s*(?P<ch>\d{1,2})\s*[.:]?\s*(?P<vs>\d{1,3})\b",
        re.IGNORECASE,
    ),
]


def detect_direct_reference(message: str) -> Optional[VerseReference]:
    for pattern in DIRECT_PATTERNS:
        match = pattern.search(message)
        if match:
            try:
                chapter = int(match.group("ch"))
                verse = int(match.group("vs"))
            except (TypeError, ValueError):
                continue
            reference = VerseReference(chapter=chapter, verse=verse)
            if is_valid_reference(reference):
                return reference
    return None


def select_reference(message: str) -> VerseReference:
    candidates = _select_with_llm(message)
    if candidates:
        choice = _choose_non_recent(candidates)
        if choice:
            _record_reference(choice)
            return choice

    fallback = _random_non_recent()
    _record_reference(fallback)
    return fallback


def _select_with_llm(message: str) -> List[VerseReference]:
    if not settings.OPENAI_API_KEY or OpenAI is None:
        return []

    prompt = _build_prompt(message)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return only JSON."},
            {"role": "user", "content": prompt},
        ],
    )

    content = completion.choices[0].message.content or "{}"
    data = _safe_parse_json(content)
    raw_candidates = data.get("candidates", [])

    references: List[VerseReference] = []
    for item in raw_candidates:
        try:
            chapter = int(item.get("chapter"))
            verse = int(item.get("verse"))
        except (TypeError, ValueError):
            continue
        reference = VerseReference(chapter=chapter, verse=verse)
        if is_valid_reference(reference):
            references.append(reference)

    return references


def _build_prompt(message: str) -> str:
    counts_text = ", ".join(f"{k}:{v}" for k, v in CHAPTER_VERSE_COUNTS.items())
    recent_text = ", ".join(RECENT_VERSES) if RECENT_VERSES else "none"

    return f"""
You are a Bhagavad Gita guide. Select relevant verses for the user's situation.
Return JSON with a "candidates" array. Each candidate must include:
chapter (1-18), verse (valid verse number), reason (short).

Chapter verse counts:
{counts_text}

Recent verses to avoid repeating if possible:
{recent_text}

User message:
{message}

Return 5 candidates ordered by relevance.
""".strip()


def _choose_non_recent(candidates: List[VerseReference]) -> Optional[VerseReference]:
    recent = set(RECENT_VERSES)
    for candidate in candidates:
        if candidate.key() not in recent:
            return candidate
    if candidates:
        return random.choice(candidates)
    return None


def _random_non_recent() -> VerseReference:
    return random_reference(exclude=set(RECENT_VERSES))


def _record_reference(reference: VerseReference) -> None:
    RECENT_VERSES.append(reference.key())


def _safe_parse_json(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            return {}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}

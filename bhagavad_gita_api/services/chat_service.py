import json
import re
from typing import Dict, Optional

from bhagavad_gita_api.config import settings
from bhagavad_gita_api.fallback_verses import VerseCard
from bhagavad_gita_api.services.blockchain_service import (
    BlockchainError,
    compute_chat_hash,
    log_chat_hash,
)
from bhagavad_gita_api.services.translation_service import (
    resolve_output_language,
    translate_inbound_text,
    translate_response_fields,
)
from bhagavad_gita_api.services.verse_service import pick_verse

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


def build_chat_response(
    message: str,
    learn_mode: bool = False,
    target_language: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    english_message, source_language = translate_inbound_text(message)
    output_language = resolve_output_language(target_language, source_language)
    verse = pick_verse(english_message)

    english_response = _generate_english_response(
        english_message=english_message,
        verse=verse,
        learn_mode=learn_mode,
    )
    localized_response = translate_response_fields(english_response, output_language)
    response_hash = compute_chat_hash(message, localized_response)

    transaction_hash = None
    try:
        transaction_hash = log_chat_hash(response_hash)
    except BlockchainError:
        transaction_hash = None

    return {
        "reference": verse.reference,
        "shloka": localized_response["shloka"],
        "meaning": localized_response["meaning"],
        "word_meaning": localized_response.get("word_meaning", ""),
        "advice": localized_response["advice"],
        "source_language": source_language,
        "response_language": output_language,
        "response_hash": response_hash,
        "transaction_hash": transaction_hash,
    }


def _generate_english_response(
    english_message: str,
    verse: VerseCard,
    learn_mode: bool,
) -> Dict[str, str]:
    if settings.OPENAI_API_KEY and OpenAI is not None:
        try:
            return _generate_with_openai(
                english_message=english_message,
                verse=verse,
                learn_mode=learn_mode,
            )
        except Exception:
            pass

    return {
        "shloka": verse.shloka,
        "meaning": verse.meaning,
        "word_meaning": verse.word_meaning if learn_mode else "",
        "advice": verse.advice,
    }


def _generate_with_openai(
    english_message: str,
    verse: VerseCard,
    learn_mode: bool,
) -> Dict[str, str]:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"""
You are Pariprashna AI, a compassionate Bhagavad Gita guide.
Use only the provided verse as the scriptural anchor.
Return valid JSON with exactly these keys:
shloka, meaning, word_meaning, advice

Rules:
- Keep the shloka exactly as provided.
- meaning should be clear, practical, and at most 2 sentences.
- advice should address the user's situation directly and at most 3 sentences.
- If learn_mode is false, return an empty string for word_meaning.
- If learn_mode is true, explain the key Sanskrit terms in simple English.

User situation:
{english_message}

Verse reference:
{verse.reference}

Shloka:
{verse.shloka}

Canonical meaning:
{verse.meaning}

Canonical word meaning:
{verse.word_meaning}

Practical guidance seed:
{verse.advice}

learn_mode:
{str(learn_mode).lower()}
""".strip()

    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You respond only with valid JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    content = completion.choices[0].message.content or "{}"
    parsed_payload = _extract_json_payload(content)

    return {
        "shloka": str(parsed_payload.get("shloka") or verse.shloka),
        "meaning": str(parsed_payload.get("meaning") or verse.meaning),
        "word_meaning": _resolve_word_meaning(parsed_payload, verse, learn_mode),
        "advice": str(parsed_payload.get("advice") or verse.advice),
    }


def _resolve_word_meaning(
    parsed_payload: Dict[str, str], verse: VerseCard, learn_mode: bool
) -> str:
    if not learn_mode:
        return ""
    return str(parsed_payload.get("word_meaning") or verse.word_meaning)


def _extract_json_payload(content: str) -> Dict[str, str]:
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

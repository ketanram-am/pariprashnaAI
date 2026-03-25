import json
import re
from typing import Dict, Optional

from sqlalchemy.orm import Session

from bhagavad_gita_api.config import settings
from bhagavad_gita_api.services.blockchain_service import (
    BlockchainError,
    compute_chat_hash,
    log_chat_hash,
)
from bhagavad_gita_api.services.gita_service import VerseReference, get_verse
from bhagavad_gita_api.services.translation_service import (
    resolve_output_language,
    translate_inbound_text,
    translate_response_fields,
)
from bhagavad_gita_api.services.verse_selector import (
    detect_direct_reference,
    select_reference,
)

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


def build_chat_response(
    message: str,
    learn_mode: bool = False,
    target_language: Optional[str] = None,
    db: Optional[Session] = None,
) -> Dict[str, Optional[str]]:
    direct_reference = detect_direct_reference(message)
    english_message, source_language = translate_inbound_text(message)
    output_language = resolve_output_language(target_language, source_language)

    if direct_reference:
        verse_reference = direct_reference
    else:
        verse_reference = select_reference(english_message)

    try:
        verse_payload = get_verse(verse_reference, db=db)
    except Exception:
        verse_payload = None
    if verse_payload:
        advice = _generate_advice(
            english_message=english_message,
            verse_reference=verse_reference,
            translation=verse_payload.translation,
        )

        english_response = {
            "shloka": verse_payload.shloka,
            "translation": verse_payload.translation,
            "word_meaning": verse_payload.word_meaning if learn_mode else "",
            "advice": advice,
        }
    else:
        english_response = _generate_fallback_response(
            english_message=english_message,
            verse_reference=verse_reference,
            learn_mode=learn_mode,
        )

    localized_response = translate_response_fields(english_response, output_language)
    response_hash = compute_chat_hash(message, localized_response)
    short_hash = response_hash.replace("0x", "")[:10]

    transaction_hash = None
    try:
        transaction_hash = log_chat_hash(response_hash)
    except BlockchainError:
        transaction_hash = None

    tx_status = "logged" if transaction_hash else "not logged"
    reference_line = f"Bhagavad Gita Chapter {verse_reference.chapter}, Verse {verse_reference.verse}"
    source_line = reference_line

    formatted = _format_response(
        shloka=localized_response["shloka"],
        reference=reference_line,
        meaning=localized_response["translation"],
        word_meaning=localized_response.get("word_meaning", ""),
        advice=localized_response["advice"],
        source=source_line,
        short_hash=short_hash,
        tx_status=tx_status,
        tx_hash=transaction_hash,
        include_word_meaning=learn_mode,
    )

    return {
        "shloka": localized_response["shloka"],
        "translation": localized_response["translation"],
        "word_meaning": localized_response.get("word_meaning", ""),
        "advice": localized_response["advice"],
        "reference": reference_line,
        "source": source_line,
        "hash": short_hash,
        "tx_status": tx_status,
        "tx_hash": transaction_hash,
        "formatted": formatted,
    }


def _generate_fallback_response(
    english_message: str,
    verse_reference: VerseReference,
    learn_mode: bool,
) -> Dict[str, str]:
    return {
        "shloka": "I am not fully certain of the exact verse reference.",
        "translation": "I am not fully certain of the exact verse reference.",
        "word_meaning": "" if not learn_mode else "I am not fully certain of the exact verse reference.",
        "advice": _fallback_advice(english_message, ""),
    }


def _generate_advice(
    english_message: str,
    verse_reference: VerseReference,
    translation: str,
) -> str:
    if settings.OPENAI_API_KEY and OpenAI is not None:
        try:
            return _generate_with_openai(
                english_message=english_message,
                verse_reference=verse_reference,
                translation=translation,
            )
        except Exception:
            pass

    return (
        _fallback_advice(english_message, translation)
    )


def _generate_with_openai(
    english_message: str,
    verse_reference: VerseReference,
    translation: str,
) -> str:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"""
You are a compassionate Bhagavad Gita guide.
Return JSON with a single key: advice.

Rules:
- advice must be 2-3 short sentences.
- keep it practical, grounded, and aligned with the verse translation.

User message:
{english_message}

Verse reference:
{verse_reference.chapter}.{verse_reference.verse}

Verse translation:
{translation}
""".strip()

    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0.5,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return only JSON."},
            {"role": "user", "content": prompt},
        ],
    )

    content = completion.choices[0].message.content or "{}"
    data = _extract_json_payload(content)
    advice = str(data.get("advice") or "").strip()
    return advice or (
        "Reflect on the verse and take one calm, purposeful action today. "
        "Consistency will bring clarity."
    )




def _format_response(
    shloka: str,
    reference: str,
    meaning: str,
    word_meaning: str,
    advice: str,
    source: str,
    short_hash: str,
    tx_status: str,
    tx_hash: Optional[str],
    include_word_meaning: bool,
) -> str:
    lines = [
        "Shloka:",
        shloka or "I am not fully certain of the exact verse reference.",
        "",
        "Reference:",
        reference,
        "",
        "Meaning:",
        meaning,
    ]

    if include_word_meaning:
        lines.extend(["", "Word Meaning:", word_meaning or ""])

    lines.extend(
        [
            "",
            "Advice:",
            advice,
            "",
            "Source:",
            source,
            "",
            f"Hash: {short_hash}",
            f"Tx: {tx_status}",
            f"Tx Hash: {tx_hash if tx_hash else 'null'}",
        ]
    )

    return "\n".join(lines)


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


def _fallback_advice(message: str, translation: str) -> str:
    lowered = message.lower()
    if any(word in lowered for word in ("stress", "pressure", "deadline", "overwork")):
        return (
            "Choose one calm, focused action instead of trying to solve everything at once. "
            "Let the verse anchor your effort, then release the anxiety about outcomes."
        )
    if any(word in lowered for word in ("anxious", "anxiety", "fear", "worried", "worry")):
        return (
            "Pause, breathe, and return to what you can actually do right now. "
            "The verse reminds you that inner steadiness is a practice, not a switch."
        )
    if any(word in lowered for word in ("confused", "lost", "stuck", "direction")):
        return (
            "Use the verse as a compass: pick one aligned step and commit to it for today. "
            "Clarity often arrives after motion begins."
        )

    return (
        "Let this verse guide one practical step you can take today. "
        "When the mind races, return to steady action and let the results unfold."
    )

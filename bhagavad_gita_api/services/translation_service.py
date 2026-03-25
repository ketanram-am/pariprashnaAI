from typing import Dict, Optional, Tuple

try:
    from deep_translator import GoogleTranslator
except ImportError:  # pragma: no cover
    GoogleTranslator = None

try:
    from langdetect import LangDetectException, detect
except ImportError:  # pragma: no cover
    LangDetectException = Exception
    detect = None


LANGUAGE_ALIASES = {
    "english": "en",
    "hindi": "hi",
    "telugu": "te",
    "kannada": "kn",
}

SUPPORTED_OUTPUT_LANGUAGES = {"en", "hi", "te", "kn"}


def normalize_language(language: Optional[str]) -> str:
    if not language:
        return "en"

    cleaned = language.strip().lower()
    if cleaned in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[cleaned]
    if "-" in cleaned:
        cleaned = cleaned.split("-", 1)[0]
    return cleaned or "en"


def translate_inbound_text(text: str) -> Tuple[str, str]:
    detected_language = detect_language(text)
    english_text = translate_text(
        text=text,
        target_language="en",
        source_language=detected_language,
    )
    return english_text, detected_language


def translate_response_fields(
    response_fields: Dict[str, str], target_language: str
) -> Dict[str, str]:
    normalized_target = normalize_language(target_language)
    if normalized_target == "en":
        return response_fields

    translated_fields = dict(response_fields)
    for field_name in ("translation", "word_meaning", "advice"):
        value = translated_fields.get(field_name, "")
        if value:
            translated_fields[field_name] = translate_text(
                text=value,
                target_language=normalized_target,
                source_language="en",
            )

    return translated_fields


def resolve_output_language(target_language: Optional[str], detected_language: str) -> str:
    if target_language:
        normalized_target = normalize_language(target_language)
        return normalized_target if normalized_target in SUPPORTED_OUTPUT_LANGUAGES else "en"

    normalized_detected = normalize_language(detected_language)
    if normalized_detected in SUPPORTED_OUTPUT_LANGUAGES:
        return normalized_detected
    return "en"


def detect_language(text: str) -> str:
    if not text.strip():
        return "en"

    if detect is None:
        return "en"

    try:
        return normalize_language(detect(text))
    except LangDetectException:
        return "en"


def translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    if not text.strip():
        return text

    normalized_source = normalize_language(source_language)
    normalized_target = normalize_language(target_language)

    if normalized_source == normalized_target:
        return text

    if GoogleTranslator is None:
        return text

    try:
        return GoogleTranslator(
            source=normalized_source if normalized_source else "auto",
            target=normalized_target,
        ).translate(text)
    except Exception:
        return text

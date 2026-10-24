#!/usr/bin/env python3
"""
Picks a random chain of languages for the "Lost in Translation" game.

Tries to read the real list of languages from the belebele dataset
(B:\\DATABASES\\Speech_Voice_Corpora\\belebele\\data\\*.jsonl). Every filename there is
a FLORES-200-style code, e.g. "khm_Khmr.jsonl" = Khmer language, Khmer script.

The belebele dataset was re-downloaded to B:\\DATABASES\\Speech_Voice_Corpora\\belebele\\data
after the 2026-09 B:\\AI Directories_Databases -> B:\\DATABASES migration. If the drive isn't
mounted (it's a removable backup volume and goes dark when unplugged), this
falls back to a built-in list of ~40 diverse languages so the game still
works offline.

Usage:
    python pick_languages.py                  # 4 random uncommon languages
    python pick_languages.py --count 6
    python pick_languages.py --seed 42         # reproducible chain
    python pick_languages.py --common          # allow common languages too
    python pick_languages.py --script Cyrl     # only languages in one script
"""

import argparse
import json
import random
import sys
from pathlib import Path

# ISO 639-3 code -> English language name (covers the codes seen in the
# belebele/FLORES-200 language set; unknown codes just fall back to
# showing the raw code, so this never needs to be 100% complete).
LANG_NAMES = {
    "acm": "Mesopotamian Arabic", "afr": "Afrikaans", "als": "Tosk Albanian",
    "amh": "Amharic", "apc": "North Levantine Arabic", "arb": "Modern Standard Arabic",
    "ars": "Najdi Arabic", "ary": "Moroccan Arabic", "arz": "Egyptian Arabic",
    "asm": "Assamese", "azj": "North Azerbaijani", "bam": "Bambara",
    "ben": "Bengali", "bod": "Tibetan", "bul": "Bulgarian", "cat": "Catalan",
    "ceb": "Cebuano", "ces": "Czech", "ckb": "Central Kurdish", "dan": "Danish",
    "deu": "German", "ell": "Greek", "eng": "English", "est": "Estonian",
    "eus": "Basque", "fin": "Finnish", "fra": "French", "fuv": "Nigerian Fulfulde",
    "gaz": "West Central Oromo", "grn": "Guarani", "guj": "Gujarati",
    "hat": "Haitian Creole", "hau": "Hausa", "heb": "Hebrew", "hin": "Hindi",
    "hrv": "Croatian", "hun": "Hungarian", "hye": "Armenian", "ibo": "Igbo",
    "ilo": "Ilocano", "ind": "Indonesian", "isl": "Icelandic", "ita": "Italian",
    "jav": "Javanese", "jpn": "Japanese", "kac": "Jingpho", "kan": "Kannada",
    "kat": "Georgian", "kaz": "Kazakh", "kea": "Kabuverdianu", "khk": "Halh Mongolian",
    "khm": "Khmer", "kin": "Kinyarwanda", "kir": "Kyrgyz", "kor": "Korean",
    "lao": "Lao", "lin": "Lingala", "lit": "Lithuanian", "lug": "Ganda",
    "luo": "Luo", "lvs": "Standard Latvian", "mal": "Malayalam", "mar": "Marathi",
    "mkd": "Macedonian", "mlt": "Maltese", "mri": "Maori", "mya": "Burmese",
    "nld": "Dutch", "nob": "Norwegian Bokmal", "npi": "Nepali", "nso": "Northern Sotho",
    "nya": "Chichewa", "ory": "Odia", "pan": "Punjabi", "pbt": "Southern Pashto",
    "pes": "Western Persian", "plt": "Plateau Malagasy", "pol": "Polish",
    "por": "Portuguese", "ron": "Romanian", "rus": "Russian", "shn": "Shan",
    "sin": "Sinhala", "slk": "Slovak", "slv": "Slovenian", "sna": "Shona",
    "snd": "Sindhi", "som": "Somali", "sot": "Southern Sotho", "spa": "Spanish",
    "srp": "Serbian", "ssw": "Swati", "sun": "Sundanese", "swe": "Swedish",
    "swh": "Swahili", "tam": "Tamil", "tel": "Telugu", "tgk": "Tajik",
    "tgl": "Tagalog", "tha": "Thai", "tir": "Tigrinya", "tsn": "Tswana",
    "tso": "Tsonga", "tur": "Turkish", "ukr": "Ukrainian", "urd": "Urdu",
    "uzn": "Northern Uzbek", "vie": "Vietnamese", "war": "Waray", "wol": "Wolof",
    "xho": "Xhosa", "yor": "Yoruba", "zho": "Chinese", "zsm": "Standard Malay",
    "zul": "Zulu",
}

SCRIPT_NAMES = {
    "Arab": "Arabic script", "Latn": "Latin script", "Ethi": "Ethiopic script",
    "Beng": "Bengali script", "Tibt": "Tibetan script", "Cyrl": "Cyrillic script",
    "Grek": "Greek script", "Gujr": "Gujarati script", "Hebr": "Hebrew script",
    "Armn": "Armenian script", "Deva": "Devanagari script", "Geor": "Georgian script",
    "Knda": "Kannada script", "Khmr": "Khmer script", "Hang": "Hangul",
    "Laoo": "Lao script", "Mlym": "Malayalam script", "Mymr": "Myanmar script",
    "Orya": "Odia script", "Guru": "Gurmukhi script", "Sinh": "Sinhala script",
    "Taml": "Tamil script", "Telu": "Telugu script", "Thai": "Thai script",
    "Hans": "Simplified Chinese", "Hant": "Traditional Chinese", "Jpan": "Japanese script",
}

# Common languages excluded by default so the chain stays interesting.
COMMON = {"eng", "spa", "fra", "deu", "ita", "por", "rus", "zho", "jpn", "kor"}

# Offline fallback if the belebele data folder isn't reachable
# (B:\ is a removable backup drive and goes dark when unplugged).
FALLBACK = [
    ("isl", "Latn"), ("khm", "Khmr"), ("zul", "Latn"), ("mlt", "Latn"),
    ("khk", "Cyrl"), ("yor", "Latn"), ("kat", "Geor"), ("hye", "Armn"),
    ("amh", "Ethi"), ("vie", "Latn"), ("mya", "Mymr"), ("eus", "Latn"), ("tgl", "Latn"),
    ("swh", "Latn"), ("hin", "Deva"), ("tha", "Thai"), ("lao", "Laoo"), ("hau", "Latn"),
    ("npi", "Deva"), ("sin", "Sinh"), ("xho", "Latn"), ("bod", "Tibt"), ("kaz", "Cyrl"),
    ("ckb", "Arab"), ("som", "Latn"), ("kin", "Latn"), ("mkd", "Cyrl"), ("kir", "Cyrl"),
    ("tam", "Taml"), ("kan", "Knda"),
]


def find_belebele_dir():
    candidate = Path(r"B:\DATABASES\Speech_Voice_Corpora\belebele\data")
    return candidate if candidate.is_dir() else None


def load_codes():
    d = find_belebele_dir()
    if d is None:
        return FALLBACK, False
    codes = []
    for f in d.glob("*.jsonl"):
        stem = f.stem  # e.g. "khm_Khmr"
        if "_" in stem:
            lang, script = stem.split("_", 1)
            codes.append((lang, script))
    return (codes if codes else FALLBACK), bool(codes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=4)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--common", action="store_true", help="allow common languages (fra/deu/spa/etc)")
    ap.add_argument("--script", type=str, default=None, help="restrict to one ISO 15924 script code, e.g. Cyrl")
    args = ap.parse_args()

    codes, live = load_codes()

    if not args.common:
        codes = [c for c in codes if c[0] not in COMMON]
    if args.script:
        codes = [c for c in codes if c[1].lower() == args.script.lower()]

    if not codes:
        print(json.dumps({"error": "no languages match the given filters"}))
        sys.exit(1)

    rng = random.Random(args.seed)
    count = min(args.count, len(codes))
    chosen = rng.sample(codes, count)

    out = []
    for lang, script in chosen:
        out.append({
            "code": f"{lang}_{script}",
            "language": LANG_NAMES.get(lang, lang),
            "script": SCRIPT_NAMES.get(script, script),
        })

    print(json.dumps({"source": "live belebele dataset" if live else "offline fallback list", "chain": out}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

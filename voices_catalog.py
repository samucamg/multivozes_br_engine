"""Consulta o catálogo real do Edge sem alterar aliases nem gerar áudio."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import edge_tts
from dotenv import load_dotenv


async def get_voices(locale=None, multilingual=False):
    """Lista vozes atuais; locale aceita idioma (pt) ou localidade (pt-BR).

    A classificação multilíngue identifica nomes MultilingualNeural publicados
    pelo Edge. Não importa vozes exclusivas do catálogo Azure Speech.
    """
    load_dotenv(Path(__file__).with_name(".env"))
    voices = await asyncio.wait_for(
        edge_tts.list_voices(proxy=os.getenv("PROXY") or None), timeout=30
    )
    if locale:
        requested = locale.casefold()
        voices = [
            voice for voice in voices
            if voice["Locale"].casefold() == requested
            or voice["Locale"].casefold().startswith(requested + "-")
        ]
    if multilingual:
        voices = [voice for voice in voices if "MultilingualNeural" in voice["ShortName"]]
    return sorted(voices, key=lambda voice: voice["ShortName"])


async def _run(args):
    # Validate aliases against the full catalog, even when output is filtered.
    if args.check_aliases:
        all_voices = await get_voices()
        available = {voice["ShortName"] for voice in all_voices}
        aliases = json.loads(Path(__file__).with_name("voices.json").read_text(encoding="utf-8"))
        missing = {alias: voice for alias, voice in aliases.items() if voice not in available}
        print(json.dumps({"aliases": aliases, "unavailable": missing}, ensure_ascii=False, indent=2))
        return 1 if missing else 0
    voices = await get_voices(args.locale, args.multilingual)
    if args.json:
        print(json.dumps(voices, ensure_ascii=False, indent=2))
    else:
        for voice in voices:
            print(f"{voice['ShortName']:<45} {voice['Gender']:<8} {voice['Locale']}")
        print(f"Total: {len(voices)}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", help="Idioma/localidade, por exemplo pt ou pt-BR")
    parser.add_argument("--multilingual", action="store_true", help="Somente MultilingualNeural")
    parser.add_argument("--json", action="store_true", help="Exibir metadados em JSON")
    parser.add_argument("--check-aliases", action="store_true", help="Verificar voices.json no catálogo completo")
    args = parser.parse_args()
    try:
        return asyncio.run(_run(args))
    except Exception as exc:
        print(f"Não foi possível consultar o catálogo Edge: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

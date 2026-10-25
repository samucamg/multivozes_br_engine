"""Contract of the local OpenAI-name adapter, not OpenAI voice equivalence."""

import json
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from config import DEFAULT_OPENAI_VOICES
import tts_handler


ROOT = Path(__file__).resolve().parents[1]


class VoiceAliasContractTests(unittest.TestCase):
    def setUp(self):
        self.aliases = json.loads((ROOT / "voices.json").read_text(encoding="utf-8"))
        fixture = json.loads((ROOT / "tests/fixtures/edge-multilingual-2026-10-25.json").read_text(encoding="utf-8"))
        self.catalog = {voice["ShortName"]: voice for voice in fixture["voices"]}

    def test_all_current_openai_aliases_resolve_to_catalogued_multilingual_voices(self):
        self.assertEqual(set(self.aliases), {
            "alloy", "ash", "ballad", "cedar", "coral", "echo", "fable",
            "marin", "nova", "onyx", "sage", "shimmer", "verse",
        })
        for alias, voice in self.aliases.items():
            with self.subTest(alias=alias):
                self.assertTrue(voice.endswith("MultilingualNeural"))
                self.assertIn(voice, self.catalog)

    def test_local_gender_profiles_use_matching_edge_catalog_genders(self):
        # These are the project's editorial profiles, not official OpenAI labels.
        male_profiles = {"ash", "ballad", "cedar", "echo", "fable", "onyx", "verse"}
        female_profiles = {"coral", "marin", "nova", "sage", "shimmer"}
        for expected, aliases in [("Male", male_profiles), ("Female", female_profiles)]:
            for alias in aliases:
                with self.subTest(alias=alias):
                    self.assertEqual(self.catalog[self.aliases[alias]]["Gender"], expected)
        # Preserve the project's Brazilian default instead of inventing a neutral Edge gender.
        self.assertEqual(self.aliases["alloy"], "pt-BR-ThalitaMultilingualNeural")

    def test_documentation_has_every_alias_and_resolved_voice(self):
        docs = (ROOT / "VOICES.md").read_text(encoding="utf-8")
        for alias, voice in self.aliases.items():
            with self.subTest(alias=alias):
                self.assertIn(f"| `{alias}` | `{voice}` |", docs)

    def test_missing_configuration_uses_complete_multilingual_fallback(self):
        with patch.object(tts_handler.Path, 'exists', return_value=False):
            fallback = tts_handler.carregar_mapeamento_vozes()
        self.assertEqual(set(fallback), set(DEFAULT_OPENAI_VOICES))
        for voice in fallback.values():
            self.assertTrue(voice.endswith('MultilingualNeural'))
            self.assertIn(voice, self.catalog)
        fallback['alloy'] = 'changed'
        self.assertEqual(DEFAULT_OPENAI_VOICES['alloy'], 'pt-BR-ThalitaMultilingualNeural')

    def test_openai_alias_cannot_silently_become_single_language(self):
        for mapping in [{'shimmer': 'pt-BR-FranciscaNeural'}, ['bad-shape'], {'alloy': None}]:
            with self.subTest(mapping=mapping):
                with patch.object(tts_handler.Path, 'exists', return_value=True), patch.object(
                    tts_handler.Path, 'open', return_value=io.StringIO(json.dumps(mapping))
                ):
                    with self.assertRaises(ValueError):
                        tts_handler.carregar_mapeamento_vozes()

    def test_custom_alias_can_still_use_regional_voice(self):
        mapping = {'narrador': 'pt-BR-AntonioNeural'}
        with patch.object(tts_handler.Path, 'exists', return_value=True), patch.object(
            tts_handler.Path, 'open', return_value=io.StringIO(json.dumps(mapping))
        ):
            self.assertEqual(tts_handler.carregar_mapeamento_vozes(), mapping)


if __name__ == "__main__":
    unittest.main()

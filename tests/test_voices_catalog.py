import asyncio
import os
import unittest
from unittest.mock import AsyncMock, patch

from voices_catalog import get_voices


class VoiceCatalogTests(unittest.IsolatedAsyncioTestCase):
    async def test_language_filter_does_not_confuse_primary_locale_with_multilingual_support(self):
        catalog = [
            {"ShortName": "en-US-AndrewMultilingualNeural", "Locale": "en-US"},
            {"ShortName": "pt-PT-RaquelNeural", "Locale": "pt-PT"},
            {"ShortName": "pt-BR-ThalitaMultilingualNeural", "Locale": "pt-BR"},
            {"ShortName": "pt-BR-FranciscaNeural", "Locale": "pt-BR"},
        ]
        with patch("voices_catalog.edge_tts.list_voices", new=AsyncMock(return_value=catalog)):
            portuguese = await get_voices("PT")
            brazilian_multilingual = await get_voices("pt-BR", multilingual=True)
            multilingual = await get_voices(multilingual=True)
        self.assertEqual(len(portuguese), 3)
        self.assertEqual([v["ShortName"] for v in brazilian_multilingual], ["pt-BR-ThalitaMultilingualNeural"])
        self.assertEqual(len(multilingual), 2)
        self.assertEqual(portuguese[0]["ShortName"], "pt-BR-FranciscaNeural")

    async def test_proxy_is_forwarded_and_upstream_failure_is_not_reported_as_empty_catalog(self):
        with patch("voices_catalog.load_dotenv"), patch.dict(os.environ, {"PROXY": "http://localhost:8888"}):
            with patch("voices_catalog.edge_tts.list_voices", new=AsyncMock(side_effect=ConnectionError("offline"))) as fetch:
                with self.assertRaises(ConnectionError):
                    await get_voices()
                fetch.assert_awaited_once_with(proxy="http://localhost:8888")

    async def test_catalog_fetch_has_a_timeout(self):
        async def fail_after_timeout(awaitable, *, timeout):
            self.assertEqual(timeout, 30)
            awaitable.close()
            raise asyncio.TimeoutError

        with patch("voices_catalog.edge_tts.list_voices", new=AsyncMock()), patch("voices_catalog.asyncio.wait_for", side_effect=fail_after_timeout):
            with self.assertRaises(asyncio.TimeoutError):
                await get_voices()


if __name__ == "__main__":
    unittest.main()

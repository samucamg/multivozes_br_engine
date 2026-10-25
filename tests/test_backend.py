import asyncio
import os
import shutil
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import main
import tts_handler

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.auth = patch.multiple(main, EXIGIR_CHAVE_API=True, CHAVE_API='test-key')
        self.auth.start()
        self.client = TestClient(main.app)
        self.headers = {'Authorization': 'Bearer test-key'}
    def tearDown(self):
        self.auth.stop()
    def post(self, data):
        return self.client.post('/v1/audio/speech', json=data, headers=self.headers)
    def test_health_is_public_and_does_not_synthesize(self):
        with patch.object(main, 'gerar_audio') as generate:
            self.assertEqual(self.client.get('/health').json(), {'status': 'ok'})
            generate.assert_not_called()
    def test_swagger_exposes_json_example_and_bearer_authorization(self):
        schema = self.client.get('/openapi.json').json()
        speech = schema['paths']['/v1/audio/speech']['post']
        body = speech['requestBody']['content']['application/json']
        self.assertEqual(body['schema']['required'], ['input'])
        self.assertEqual(set(body['example']), {'input', 'model', 'voice', 'response_format', 'speed'})
        self.assertIn({'BearerAuth': []}, speech['security'])
        self.assertEqual(schema['components']['securitySchemes']['BearerAuth']['scheme'], 'bearer')
        self.assertIn('audio/mpeg', speech['responses']['200']['content'])
        self.assertNotIn('security', schema['paths']['/health']['get'])
    def test_auth_can_be_disabled_without_bearer_header(self):
        with patch.object(main, 'EXIGIR_CHAVE_API', False):
            response = self.client.post('/v1/audio/speech', json={})
            self.assertEqual(response.status_code, 400)
    def test_authentication(self):
        for token in ['', 'Bearer wrong', 'Bearer test-keyBearer wrong', 'Bearer chave-acentuada-á']:
            # HTTP header transport is ASCII; test Unicode directly in dependency separately.
            if not token.isascii():
                continue
            response = self.client.post('/v1/audio/speech', json={'input': 'Oi'}, headers={'Authorization': token})
            self.assertEqual(response.status_code, 401)
        with patch.object(main, 'CHAVE_API', None):
            self.assertEqual(self.post({'input': 'Oi'}).status_code, 503)
    def test_bad_requests_remain_client_errors(self):
        for data in [None, [], {}, {'input': 42}, {'input': ' '}, {'input': '🙂'}, {'input': 'Oi','speed': True}, {'input': 'Oi','speed': 'nan'}, {'input': 'Oi','speed': 3}, {'input': 'Oi','voice': '../bad'}, {'input': 'Oi','response_format': 'exe'}]:
            with self.subTest(data=data):
                self.assertEqual(self.post(data).status_code, 400)
        self.assertEqual(self.client.post('/v1/audio/speech', content='{broken', headers=self.headers).status_code, 400)
    def test_input_and_body_limits(self):
        with patch.object(main, 'MAX_INPUT_CHARS', 3):
            self.assertEqual(self.post({'input': 'Muito texto'}).status_code, 413)
        with patch.object(main, 'MAX_REQUEST_BYTES', 3):
            self.assertEqual(self.post({'input':'Oi'}).status_code, 413)
    def test_deeply_nested_json_is_a_client_error_without_synthesis(self):
        payload = '{"input":"Oi","unused":' + '[' * 8000 + '0' + ']' * 8000 + '}'
        with patch.object(main, 'gerar_audio', new=AsyncMock()) as generate:
            response = self.client.post('/v1/audio/speech', content=payload, headers=self.headers)
            self.assertEqual(response.status_code, 400)
            generate.assert_not_awaited()
    def test_upstream_error_is_sanitized(self):
        with patch.object(main,'gerar_audio',new=AsyncMock(side_effect=RuntimeError('secret://password'))):
            response = self.post({'input':'Oi'})
            self.assertEqual(response.status_code, 502)
            self.assertNotIn('password',response.text)
    def test_timeout_and_capacity(self):
        async def slow(*args):
            await asyncio.sleep(1)
        with patch.object(main,'gerar_audio',new=slow), patch.object(main,'TTS_TIMEOUT_SECONDS',0.001):
            self.assertEqual(self.post({'input':'Oi'}).status_code,504)
        with patch.object(main,'_synthesis_slots',asyncio.Semaphore(0)):
            self.assertEqual(self.post({'input':'Oi'}).status_code,503)
    def test_stream_response_cleanup_normalization_and_script_locale(self):
        fd,path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
        Path(path).write_bytes(b'fake-audio-for-http-contract')
        with patch.object(main,'gerar_audio',new=AsyncMock(return_value=path)) as generate:
            response=self.post({'input':'**Oi**','voice':'sr-Latn-RS-NicholasNeural','response_format':'MP3'})
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.headers['content-type'],'audio/mpeg')
            generate.assert_awaited_once_with('Oi','sr-Latn-RS-NicholasNeural','mp3',1.0)
        self.assertFalse(Path(path).exists())
    def test_model_field_remains_ignored_for_existing_clients(self):
        for model in ['gpt-4o-mini-tts', 'tts-1-1106', 'custom-legacy-model', '', None, []]:
            descriptor, path = tempfile.mkstemp(suffix='.mp3')
            os.close(descriptor)
            Path(path).write_bytes(b'audio')
            with patch.object(main, 'gerar_audio', new=AsyncMock(return_value=path)):
                self.assertEqual(self.post({'input': 'Oi', 'model': model}).status_code, 200)
            self.assertFalse(Path(path).exists())
    def test_voices_catalog_filter_and_auth(self):
        self.assertEqual(self.client.get('/v1/audio/voices').status_code,401)
        with patch('voices_catalog.get_voices',new=AsyncMock(return_value=[{'ShortName':'test'}])) as voices:
            response=self.client.get('/v1/audio/voices?locale=pt-BR&multilingual=true',headers=self.headers)
            self.assertEqual(response.json(),{'data':[{'ShortName':'test'}]})
            voices.assert_awaited_once_with(locale='pt-BR',multilingual=True)

class AudioTests(unittest.IsolatedAsyncioTestCase):
    async def test_response_send_failure_or_cancellation_removes_audio(self):
        for error in [RuntimeError('connection closed'), asyncio.CancelledError()]:
            descriptor, path = tempfile.mkstemp(suffix='.mp3')
            os.close(descriptor)
            Path(path).write_bytes(b'audio')
            response = main.TemporaryAudioResponse(path, media_type='audio/mpeg')
            with self.assertRaises(type(error)):
                await response(
                    {'type': 'http', 'method': 'GET', 'headers': [], 'extensions': {}, 'asgi': {'spec_version': '2.4'}},
                    AsyncMock(), AsyncMock(side_effect=error),
                )
            self.assertFalse(Path(path).exists())

    def test_rate_rounds_instead_of_truncating_float_representation(self):
        for speed, expected in [(0.9, '-10%'), (1.15, '+15%'), (1.2, '+20%'), (0.25, '-75%'), (1.0, '+0%'), (2.0, '+100%')]:
            self.assertEqual(tts_handler.velocidade_para_taxa(speed), expected)
    async def test_conversion_cancellation_terminates_ffmpeg(self):
        process = AsyncMock()
        process.returncode = None
        process.kill = unittest.mock.Mock()
        process.wait.side_effect = [asyncio.CancelledError(), 1]
        with patch.object(tts_handler.shutil, 'which', return_value='ffmpeg'), patch.object(tts_handler.asyncio, 'create_subprocess_exec', return_value=process):
            with self.assertRaises(asyncio.CancelledError):
                await tts_handler._convert('source', 'destination', 'wav')
        process.kill.assert_called_once()
        self.assertEqual(process.wait.await_count, 2)

    async def test_conversion_failure_removes_both_files(self):
        created = []
        original = tts_handler._temporary_path
        def track(suffix):
            path = original(suffix)
            created.append(path)
            return path
        async def save(path):
            Path(path).write_bytes(b'partial')
        communicator = AsyncMock()
        communicator.save.side_effect = save
        with patch.object(tts_handler, '_temporary_path', side_effect=track), patch.object(tts_handler.edge_tts, 'Communicate', return_value=communicator), patch.object(tts_handler.shutil, 'which', return_value=None):
            with self.assertRaises(RuntimeError):
                await tts_handler.gerar_audio('Oi', 'alloy', 'wav', 1.0)
        self.assertEqual(len(created), 2)
        self.assertTrue(all(not Path(path).exists() for path in created))

    async def test_synthesis_cancellation_removes_partial_files(self):
        created=[]
        original=tts_handler._temporary_path
        def track(suffix):
            path=original(suffix); created.append(path); return path
        async def cancel(path):
            Path(path).write_bytes(b'partial')
            raise asyncio.CancelledError
        communicator=AsyncMock()
        communicator.save.side_effect=cancel
        with patch.object(tts_handler,'_temporary_path',side_effect=track), patch.object(tts_handler.edge_tts,'Communicate',return_value=communicator):
            with self.assertRaises(asyncio.CancelledError):
                await tts_handler.gerar_audio('Oi','alloy','mp3',1.0)
        self.assertTrue(created)
        self.assertTrue(all(not Path(path).exists() for path in created))
    async def test_mp3_does_not_need_ffmpeg(self):
        async def save(path): Path(path).write_bytes(b'fake-audio')
        communicator=AsyncMock(); communicator.save.side_effect=save
        with patch.object(tts_handler.edge_tts,'Communicate',return_value=communicator), patch.object(tts_handler.shutil,'which',return_value=None):
            path=await tts_handler.gerar_audio('Oi','alloy','mp3',1.0)
            self.assertEqual(Path(path).read_bytes(),b'fake-audio')
            Path(path).unlink()
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg required for codec verification')
    async def test_real_ffmpeg_formats_from_local_fixture(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'fixture.wav'
            with wave.open(str(source),'wb') as audio:
                audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(24000)
                audio.writeframes(b'\0\0'*2400)
            signatures={'wav':b'RIFF','flac':b'fLaC','opus':b'OggS'}
            for format_name in tts_handler.CONVERSION_ARGS:
                destination=Path(folder)/('out.'+format_name)
                await tts_handler._convert(str(source),str(destination),format_name)
                self.assertGreater(destination.stat().st_size,0)
                if format_name in signatures:
                    self.assertTrue(destination.read_bytes().startswith(signatures[format_name]))
                if format_name=='pcm':
                    self.assertEqual(destination.stat().st_size,4800)
                if format_name=='aac':
                    self.assertEqual(destination.read_bytes()[0],255)

if __name__=='__main__': unittest.main()

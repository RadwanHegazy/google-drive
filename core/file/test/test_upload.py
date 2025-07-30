from django.core.cache import cache
from channels.testing import ChannelsLiveServerTestCase
from channels.testing import WebsocketCommunicator
from globals.test_objects import create_headers, create_user
from core.asgi import application
from channels.db import database_sync_to_async

class TestWebSocketConsumer(ChannelsLiveServerTestCase):

    def get_application(self):
        return application
    
    @staticmethod
    def generate_chunks(size_mb: float) -> bytes:
        size_bytes = int(size_mb * 1024 * 1024) 
        return b'\x00' * size_bytes 

    @staticmethod
    def generate_txt_chunks(size_mb: float) -> bytes:
        size_bytes = int(size_mb * 1024 * 1024) 
        return b'ilovepython' * size_bytes 


    @staticmethod
    def split_into_chunks(data: bytes, max_chunk_size_mb: float = 0.5) -> list[bytes]:
        max_chunk_bytes = int(max_chunk_size_mb * 1024 * 1024)
        chunks = []
        
        for i in range(0, len(data), max_chunk_bytes):
            chunk = data[i:i + max_chunk_bytes]
            chunks.append(chunk)
        
        return chunks

    async def test_websocket_without_tokens(self):
        communicator = WebsocketCommunicator(
            self.get_application(),
            "/ws/session/"
        )
        connected, _ = await communicator.connect()
        self.assertFalse(connected)

        await communicator.disconnect()
        
    async def test_websocket_with_tokens(self):
        headers = await database_sync_to_async(create_headers)()
        headers = headers['Authorization'].split(" ")[1]

        communicator = WebsocketCommunicator(
            self.get_application(),
            f"/ws/session/?token={headers}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_websocket_session_start(self):
        headers = await database_sync_to_async(create_headers)()
        headers = headers['Authorization'].split(" ")[1]

        communicator = WebsocketCommunicator(
            self.get_application(),
            f"/ws/session/?token={headers}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'filename': 'test_file.txt',
            'content_type': 'text/plain'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 201)
        await communicator.disconnect()

    async def test_websocket_add_chunks(self):
        user = await database_sync_to_async(create_user)()
        headers = await database_sync_to_async(create_headers)(user)
        headers = headers['Authorization'].split(" ")[1]

        communicator = WebsocketCommunicator(
            self.get_application(),
            f"/ws/session/?token={headers}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'filename': 'test_file.txt',
            'content_type': 'text/plain'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 201)

        # Sending a chunk
        chunk_data = b'100'
        await communicator.send_to(
            bytes_data=chunk_data
        )

        # Receiving confirmation of chunk addition
        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 200)

        head = cache.get(f"chunk_head_{user.id}", None)
        self.assertIsNotNone(head)
        self.assertIsNotNone(head.get('next', None))
        chunk_data = cache.get(head['next'], None)
        self.assertIsNotNone(chunk_data)
        await communicator.disconnect()
    
    async def test_websocket_send_big_chunk(self):
        user = await database_sync_to_async(create_user)()
        headers = await database_sync_to_async(create_headers)(user)
        headers = headers['Authorization'].split(" ")[1]

        communicator = WebsocketCommunicator(
            self.get_application(),
            f"/ws/session/?token={headers}"
        )
        connected, _ = await communicator.connect(timeout=10000)
        self.assertTrue(connected)

        await communicator.send_json_to({
            'filename': 'test_file.txt',
            'content_type': 'text/plain'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 201)

        # Sending a chunk
        chunk = self.generate_chunks(1.0)
        await communicator.send_to(
            bytes_data=chunk
        )
        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 400)

    async def test_websocket_send_multiable_chunks(self):
        user = await database_sync_to_async(create_user)()
        headers = await database_sync_to_async(create_headers)(user)
        headers = headers['Authorization'].split(" ")[1]

        communicator = WebsocketCommunicator(
            self.get_application(),
            f"/ws/session/?token={headers}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'filename': 'test_file.txt',
            'content_type': 'text/plain'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 201)

        # Sending a chunk
        chunk_data = self.generate_txt_chunks(0.1)
        chunks_list = self.split_into_chunks(chunk_data, max_chunk_size_mb=0.01)
        total_sended_chunks = 0
        for chunk in chunks_list:
            total_sended_chunks += len(chunk) / (1024 * 1024)  # in MB
            await communicator.send_to(
                bytes_data=chunk
            )
            response = await communicator.receive_json_from()
            self.assertEqual(response['status'], 200)


        next = f"chunk_head_{user.id}"
        while next:
            next_chanks = cache.get(next, None)
            self.assertIsNotNone(next_chanks)
            next = next_chanks.get('next', None)

        await communicator.send_json_to({
            'status': 'done'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['status'], 204)

        await communicator.disconnect()
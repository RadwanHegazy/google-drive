from channels.generic.websocket import WebsocketConsumer
import json
from globals.chunking.session_handler import SessionHandler

class SessionConsumer (WebsocketConsumer) :

    def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            self.close()
            return

        self.accept()
        self.session_handler = SessionHandler(self.user.id)

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data) if text_data else {}
       
       
        if 'filename' and 'content_type' in text_data_json.keys():
            filename = text_data_json['filename']
            content_type = text_data_json['content_type']
            self.session_handler.start_session(filename, content_type)
            self.send(text_data=json.dumps({
                'message': 'Session created successfully.',
                'status' : 201
            }))
        
        if 'status' in text_data_json.keys():
            if text_data_json['status'] == 'done':
                self.session_handler.process_chunks()
                self.send(text_data=json.dumps({
                    'status' : 204
                }))
                return
            
        
        if bytes_data:
            # check if size more than 512kb
            if len(bytes_data) > 512 * 1024:
                self.send(text_data=json.dumps({
                    'message': 'Chunk size exceeds limit.',
                    'status': 400
                }))
                return
            self.session_handler.add_chunk(
                chunk=bytes_data,
                chunk_size_in_kb=len(bytes_data) / 1024
            )
            self.send(text_data=json.dumps({
                'message': 'Recived chunks successfully.',
                'status' : 200
            }))
    

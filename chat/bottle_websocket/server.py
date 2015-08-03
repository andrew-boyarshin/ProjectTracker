from bottle import ServerAdapter
from gevent import pywsgi
from chat.geventwebsocket.handler import WebSocketHandler

class GeventWebSocketServer(ServerAdapter):
    def run(self, handler):
        while True:
            pywsgi.WSGIServer((self.host, self.port), handler, handler_class=WebSocketHandler).serve_forever()

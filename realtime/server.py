
import os
import json
import hmac

import tornado.ioloop
import tornado.web
import tornado.websocket

clients = set()

REALTIME_SECRET = os.getenv(
    "NOTESPACE_REALTIME_SECRET",
    "notespace-local-dev-secret"
)


def diffuser_evenement(event):
    message = json.dumps(event, ensure_ascii=False)

    for client in list(clients):
        try:
            client.write_message(message)
        except tornado.websocket.WebSocketClosedError:
            clients.discard(client)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({
            "application": "NoteSpace",
            "service": "Tornado",
            "status": "running",
            "websocket": "/ws",
            "publish": "/publish"
        })


class PublishHandler(tornado.web.RequestHandler):
    def post(self):
        secret = self.request.headers.get(
            "X-Notespace-Secret", ""
        )

        if not hmac.compare_digest(secret, REALTIME_SECRET):
            raise tornado.web.HTTPError(403, "Accès refusé")

        try:
            event = json.loads(self.request.body)

            if not isinstance(event, dict):
                raise ValueError("Événement invalide")

            diffuser_evenement(event)

            self.write({
                "status": "sent",
                "connected_clients": len(clients)
            })

        except (json.JSONDecodeError, ValueError):
            raise tornado.web.HTTPError(400, "JSON invalide")


class NoteSpaceWebSocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        clients.add(self)
        print("Nouvelle connexion WebSocket")
        self.write_message(json.dumps({
            "type": "connection",
            "message": "Connecté à NoteSpace Realtime"
        }))

    def on_message(self, message):
        try:
            data = json.loads(message)

            if not isinstance(data, dict):
                raise ValueError("Message invalide")

            diffuser_evenement({
                "type": "message",
                "message": data.get(
                    "message",
                    "Nouvelle activité"
                )
            })

        except (json.JSONDecodeError, ValueError):
            self.write_message(json.dumps({
                "error": "Message JSON invalide"
            }))

    def on_close(self):
        clients.discard(self)
        print("Connexion WebSocket fermée")


def make_app():
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/ws", NoteSpaceWebSocket),
        (r"/publish", PublishHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8765, address="127.0.0.1")

    print("NoteSpace Tornado : http://127.0.0.1:8765")
    print("WebSocket : ws://127.0.0.1:8765/ws")
    print("Publication interne : http://127.0.0.1:8765/publish")

    tornado.ioloop.IOLoop.current().start()

import json
import threading
import uuid

import log
import pika
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.resource import Resource, WebSocketApplication

logger = log.getLogger("chat")


def publish(body, exchange):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout")
    channel.basic_publish(
        exchange=exchange, routing_key="", body=body,
    )
    connection.close()


def listener(callback, exchange):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout")
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name)

    channel.basic_consume(
        callback, queue=queue_name, no_ack=True,
    )
    channel.start_consuming()


class Chat(WebSocketApplication):
    def on_open(self, *args, **kwargs):
        self.userid = uuid.uuid4()
        listener_thread = threading.Thread(
            target=listener, args=(self.on_broadcast, "room1")
        )
        listener_thread.setDaemon(True)
        listener_thread.start()

    def on_message(self, message, *args, **kwargs):
        if not message:
            return

        data = json.loads(message)
        data["user"] = self.userid.hex
        body = json.dumps(data)
        # logger.info('On published %s' % body)
        publish(body, "room1")

    def on_broadcast(self, ch, method, properties, body):
        # logger.info('On broadcast %s' % body)
        data = json.loads(str(body, "utf-8"))
        self.ws.send(json.dumps(data))


def index(environ, start_response):
    start_response("200 OK", [("Content-type", "text/html")])
    html = open("index.html", "rb").read()
    return [html]


application = Resource([("^/chat", Chat), ("^/", index)])


if __name__ == "__main__":
    WSGIServer(
        "{}:{}".format("0.0.0.0", 8000), application, handler_class=WebSocketHandler
    ).serve_forever()

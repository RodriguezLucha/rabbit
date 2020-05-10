from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import pika
import time

import _thread

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


def consume_now(socketio):

    @socketio.on('connect')
    def connected():
        print("its connected")

    print("STARTED")

    def callback(ch, method, properties, body):
        print(body)
        socketio.emit('message2', str(body))
        print("emit the event done.")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='message')
    channel.basic_consume(
        queue='message', on_message_callback=callback, auto_ack=True)

    print("START CONSUMING.")
    channel.start_consuming()
    print("DONE CONSUMING.")


if __name__ == '__main__':
    _thread.start_new_thread(consume_now, (socketio, ))
    socketio.run(app, port=5001)

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('message')
def handle_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))

    channel = connection.channel()
    channel.queue_declare(queue='message')
    channel.basic_publish(exchange='',
                          routing_key='message',
                          body=str(message))
    connection.close()

    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)

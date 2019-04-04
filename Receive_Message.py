import pika
from Config import *

credentials = pika.PlainCredentials(
    username=Username,
    password=Password)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=Host,
    credentials = credentials
))

channel = connection.channel()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(
    queue=Queue,
    auto_ack=True,
    on_message_callback=callback)

print(" [*] Waiting for messages.")
channel.start_consuming()
import pika
from Config import *

credentials = pika.PlainCredentials(
    username = Username,
    password = Password)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = Host,
    credentials = credentials
))

channel = connection.channel()

def send_message():
    channel.basic_publish(
        exchange = "", #(AMQP Default) defaults to Direct
        routing_key = Queue,
        body = "Test Message")

# Sends 100 Test Messages
for _ in range(100):
    send_message()
    print("Sent Message", _, "of", 100 ) 
    
connection.close
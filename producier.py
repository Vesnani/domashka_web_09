import pika
import random
from faker import Faker
from mongoengine import connect
from models import Contact

connect(host="mongodb+srv://vesnanifields:ZkzSOjxLQl5TYTpU@cluster0.pfhaw6o.mongodb.net/?retryWrites=true&w=majority")


rabbitmq_params = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(rabbitmq_params)
channel = connection.channel()


channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

fake = Faker()

num_contacts = 10

for _ in range(num_contacts):
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        preferred_method=random.choice(['email', 'sms']),
        message_sent=False
    )
    contact.save()
    print(f"Saved contact: {contact.fullname}")

    if contact.preferred_method == 'email':
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id).encode())
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact.id).encode())

print("Finished producing contacts")
connection.close()

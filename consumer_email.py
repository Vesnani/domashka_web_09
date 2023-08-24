import pika
from mongoengine import connect
from models import Contact

connect(host="mongodb+srv://vesnanifields:ZkzSOjxLQl5TYTpU@cluster0.pfhaw6o.mongodb.net/?retryWrites=true&w=majority")


rabbitmq_params = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(rabbitmq_params)
channel = connection.channel()


channel.queue_declare(queue='email_queue')

def send_email(contact):
    print(f"Sending email to {contact.email}")

    contact.message_sent = True
    contact.save()
    print(f"Email sent to {contact.email}")

def process_email(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact and contact.preferred_method == 'email':
        print(f"Processing email for contact: {contact.fullname}")
        send_email(contact)
        print(f"Email processed for contact: {contact.fullname}")

channel.basic_consume(queue='email_queue', on_message_callback=process_email, auto_ack=True)
print("Waiting for email messages. To exit press CTRL+C")
channel.start_consuming()

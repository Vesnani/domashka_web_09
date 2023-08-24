import pika
from mongoengine import connect
from models import Contact


connect(host="mongodb+srv://vesnanifields:ZkzSOjxLQl5TYTpU@cluster0.pfhaw6o.mongodb.net/?retryWrites=true&w=majority")


rabbitmq_params = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(rabbitmq_params)
channel = connection.channel()


channel.queue_declare(queue='sms_queue')

def send_sms(contact):
    print(f"Sending SMS to {contact.phone_number}")

    contact.message_sent = True
    contact.save()
    print(f"SMS sent to {contact.phone_number}")

def process_sms(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact and contact.preferred_method == 'sms':
        print(f"Processing SMS for contact: {contact.fullname}")
        send_sms(contact)
        print(f"SMS processed for contact: {contact.fullname}")

channel.basic_consume(queue='sms_queue', on_message_callback=process_sms, auto_ack=True)
print("Waiting for SMS messages. To exit press CTRL+C")
channel.start_consuming()

from mongoengine import *

connect(host="mongodb+srv://vesnanifields:ZkzSOjxLQl5TYTpU@cluster0.pfhaw6o.mongodb.net/?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True}


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)
    phone_number = StringField()
    preferred_method = StringField(choices=["email", "sms"], default="email")
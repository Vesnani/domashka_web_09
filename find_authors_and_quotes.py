import re
import redis
from mongoengine import *
from models import Author, Quote
from redis_lru import RedisLRU

connect(host="mongodb+srv://vesnanifields:ZkzSOjxLQl5TYTpU@cluster0.pfhaw6o.mongodb.net/?retryWrites=true&w=majority")

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
cache = RedisLRU(redis_client)

def process_query_value(query_value):
    query_value = re.sub(r'^st$', 'Steve Martin', query_value)
    query_value = re.sub(r'^li$', 'life', query_value)
    return query_value


@cache
def search_quotes(query_type, query_value):
    query_value = process_query_value(query_value)
    if query_type == 'name':
        author = Author.objects(fullname=query_value).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
        else:
            return []

    elif query_type == 'tag':
        quotes = Quote.objects(tags=query_value)
        return quotes

    elif query_type == 'tags':
        tags = query_value.split(',')
        quotes = Quote.objects(tags__in=tags)
        return quotes

    else:
        return []

def main():
    while True:
        command = input("Enter command: ").strip()
        if command == 'exit':
            print("Exiting the script.")
            break
        else:
            command_parts = command.split(':', 1)
            if len(command_parts) == 2:
                query_type = command_parts[0].strip()
                query_value = command_parts[1].strip()
                quotes = search_quotes(query_type, query_value)
                for quote in quotes:
                    print(quote.quote)
            else:
                print("Invalid command format. Please use 'command: value' format.")


if __name__ == '__main__':
    main()

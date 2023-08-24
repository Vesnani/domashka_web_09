import json
import requests
from bs4 import BeautifulSoup

base_url = 'http://quotes.toscrape.com'


def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    author_data = {}

    author_details = soup.select('.author-details')[0]

    author_data['fullname'] = author_details.select_one('.author-title').get_text(strip=True)
    author_data['born_date'] = author_details.select_one('.author-born-date').get_text(strip=True)
    author_data['born_location'] = author_details.select_one('.author-born-location').get_text(strip=True)
    author_data['description'] = author_details.select_one('.author-description').get_text(strip=True)

    return author_data


def main():
    all_quotes = []
    all_authors = []

    next_page = base_url
    while next_page:
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        for quote in soup.select('.quote'):
            quote_data = {
                'tags': [tag.get_text(strip=True) for tag in quote.select('.tag')],
                'author': quote.select_one('.author').get_text(strip=True),
                'quote': quote.select_one('.text').get_text(strip=True)
            }
            all_quotes.append(quote_data)

            author_url = base_url + quote.select_one('.author + a')['href']
            author_info = get_author_info(author_url)
            all_authors.append(author_info)

        next_button = soup.select_one('.next > a')
        next_page = base_url + next_button['href'] if next_button else None

    with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
        json.dump(all_quotes, quotes_file, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as authors_file:
        json.dump(all_authors, authors_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()


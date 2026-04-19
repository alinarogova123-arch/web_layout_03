from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import json
import os
import math


def get_books():
    with open("meta_data.json", "r", encoding='utf-8') as my_file:
        books = json.load(my_file)
    return books


def on_reload(books_for_pages, template, page_count):
    for page_number, books_for_page in enumerate(books_for_pages, 1):
        books_of_two = list(chunked(books_for_page, 2))
        rendered_page = template.render(
        books_of_two=books_of_two,
        page_number=page_number,
        page_count=page_count
        )
        with open(f'pages/index{page_number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    os.makedirs("pages", exist_ok=True)
    books = get_books()
    books_for_pages = list(chunked(books, 20))
    page_count=math.ceil(len(books) / 20)
    env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    on_reload(books_for_pages, template, page_count)
    server = Server()
    server.watch('template.html', on_reload(books_for_pages, template, page_count))
    server.serve(root='.')


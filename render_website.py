from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import json
import os


os.makedirs("pages", exist_ok=True)


with open("meta_data.json", "r", encoding='utf-8') as my_file:
    books = json.loads(my_file.read())

books_for_pages = list(chunked(books, 20))

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def on_reload():
    template = env.get_template('template.html')
    for num_page, books_for_page in enumerate(books_for_pages, 1):
        books_of_two = list(chunked(books_for_page, 2))
        rendered_page = template.render(
        books_of_two=books_of_two,
        )
        with open(f'pages/index{num_page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='pages')
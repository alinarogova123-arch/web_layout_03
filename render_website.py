from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


with open("meta_data.json", "r", encoding='utf-8') as my_file:
    books = json.loads(my_file.read())

# meta_data = json.loads(meta_data_json)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    books=books,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
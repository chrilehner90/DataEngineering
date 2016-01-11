import config
import sys
import os
from elasticsearch import Elasticsearch
es = Elasticsearch()

def add_books():
    for file_name in os.listdir('./books/'):
        with open('./books/' + str(file_name)) as f:
            book = str(unicode(f.read(), errors="ignore"))
            
            res = es.index(index="book-index", doc_type='book', id=file_name, body=book)


if __name__ == "__main__":

    add_books()

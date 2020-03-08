import codecs
import json
import os
import os.path
import random
import re

from bs4 import BeautifulSoup

from DataManager.datamanager import document_path, save_docs, download_and_extract
from Parser.query_parser import Parser


def get_documents(file):
    text = "".join([i for i in file])
    docs = []
    st, en = 1, 2
    while st < en:
        st, en = text.find('<REUTERS'), text.find('</REUTERS>')
        if st == -1:
            break
        docs.append(text[st:en + 10])
        text = text[en + 2:]
    return docs





def process_docs(docs):
    return list(map(lambda x: BeautifulSoup(x, features="html.parser").get_text(), docs))


class Crawler:
    def __init__(self, downloaded=False):
        self.parser = Parser()
        self.url = None
        self.downloaded = downloaded
        self.docs = []

    def get_collection(self):

        if os.path.isfile('collection.json'):
            with open('collection.json', 'r') as fd:
                return json.load(fd)
        if not self.downloaded:
            download_and_extract(
                'https://archive.ics.uci.edu/ml/machine-learning-databases/reuters21578-mld/reuters21578.tar.gz',
                './.misc/reuters.tar.gz')
            self.downloaded = True

        pattern = re.compile(".+\.sgm$")
        for file in os.listdir("./.misc/files"):
            file = './.misc/files/' + file
            if not pattern.match(file):
                continue

            with codecs.open(file, 'r', encoding='utf-8', errors='ignore') as f:
                docs = get_documents(f)
                docs = process_docs(docs)
                save_docs('./.misc/docs', docs, file[:-4])
                self.docs.extend(list(
                    zip([f"{document_path('./.misc/docs/', file[:-4])}/{str(i + 1)}.txt" for i in range(len(docs))],
                        docs)))



    def retrieve_docs(self):
        # for now random

        path, doc = random.choice(self.docs)
        return str(path) + "\n" + str(doc)


if __name__ == '__main__':
    crawler = Crawler(downloaded=True)
    crawler.get_collection()
    print(crawler.retrieve_docs())

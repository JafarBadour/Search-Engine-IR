import codecs
import json
import os
import os.path
import re
import tarfile
import urllib.request as req
import random
from bs4 import BeautifulSoup

from Parser.query_parser import Parser


def download_and_extract(url, filepath):
    tolerant_mkdir('.misc')
    tolerant_mkdir('.misc/docs')
    tolerant_mkdir('.misc/files')
    if os.path.isfile(filepath):
        return 0
    else:
        req.urlretrieve(url, filepath)
    tf = tarfile.open("./.misc/reuters.tar.gz")
    tf.extractall('./.misc/files/')


def tolerant_mkdir(path):
    try:
        os.mkdir(path)
        return 'Success'
    except:
        return 'Failed'


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


def save_docs(path, docs, directory):
    path = os.path.join(path, os.path.basename(directory))
    print(f"file {os.path.basename(directory)} docs are being processed and extracted to {path}")

    tolerant_mkdir(path)
    for i in range(1, len(docs) + 1):
        newpath = os.path.join(path, str(i) + ".txt")
        with open(newpath, 'w') as f:
            f.write(docs[i - 1])


class Crawler:
    def __init__(self, downloaded=False):
        self.parser = Parser()
        self.url = None
        self.downloaded = downloaded
        self.docs = []

    def process_docs(self, docs, f):
        collection = [[]]
        for line in f:
            soup = BeautifulSoup(line)
            collection[-1].extend(self.parser.preprocess(soup.get_text()))

    def save_collection(self):
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
                save_docs('./.misc/docs', docs, file[:-4])
                self.docs.extend(docs)

    def retrieve_docs(self):
        # for now random
        return random.choice(self.docs)

if __name__ == '__main__':
    crawler = Crawler(downloaded=True)
    crawler.save_collection()
    print(crawler.retrieve_docs())

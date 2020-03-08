import os
import os.path
import random as rnd
import tarfile
import urllib.request as req
import json



def document_path(path, directory):
    return os.path.join(path, os.path.basename(directory))


def tolerant_mkdir(path):
    try:
        os.mkdir(path)
        return 'Success'
    except:
        return 'Failed'


def save_docs(path, docs, directory):
    path = document_path(path, directory)
    print(f"file {os.path.basename(directory)} docs are being processed and extracted to {path}")

    tolerant_mkdir(path)
    for i in range(1, len(docs) + 1):
        newpath = os.path.join(path, str(i) + ".txt")
        with open(newpath, 'w') as f:
            f.write(docs[i - 1])


def read_doc(path):
    res = 'Failed'
    print(path)
    with open(path, 'r') as f:
        res = f.readlines()

    return "\n".join(res)


def save_doc(path, doc):
    with open(path, 'w') as f:
        f.write(doc)


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


def get_parent(path):
    path = os.path.join('.', path)

    parent_path = os.path.dirname(path)
    return parent_path


def get_cached():
    a, b = {}, {}
    if os.path.isfile('inverted_word_index.json'):
        with open('inverted_word_index.json', 'r') as fd:
            a = json.load(fd)
            a = {vi: set(a[vi]) for vi in a.keys()}
    if os.path.isfile('ngram_word_index.json'):
        with open('ngram_word_index.json', 'r') as fd:
            b = json.load(fd)
            b = {vi: set(b[vi]) for vi in b.keys()}
    return a, b


def write_cached(inverted_word_index, ngram_word_index):
    a, b = inverted_word_index, ngram_word_index
    print(type(a), type(b))
    with open('inverted_word_index.json', 'w') as fd:
        data = {vi: list(a[vi]) for vi in a.keys()}
        a = json.dump(data, fd)
    with open('ngram_word_index.json', 'w') as fd:
        data = {vi: list(b[vi]) for vi in b.keys()}
        json.dump(data, fd)
    return 'Success'


def save_set(path, data):
    with open(f'{path}.json', 'w') as fd:
        json.dump(list(data), fd)


def fetch_set(path):
    if os.path.isfile(f'{path}.json'):
        with open(f'{path}.json', 'r') as fd:
            a = json.load(fd)
            a = set(a)
            return a
    return set([])


def merge(dic1, dic2):
    if len(dic1) < len(dic2):
        dic2, dic1 = dic1, dic2
    dic3 = dic1.copy()
    for key in dic2.keys():
        d = dic3.setdefault(key, set([]))
        dic3[key] = d.union(dic2[key])
    return dic3


class DBmanager:
    def __init__(self):
        self.root = '.misc/db/'
        tolerant_mkdir('.misc')
        tolerant_mkdir('.misc/db')

    def dump(self, aux_index, word):
        dic1 = fetch_set(self.root + f"{word}")
        save_set(self.root + f"{word}", dic1.union(aux_index[word]))

    def update_aux_index(self, aux_index, word):
        dic1 = fetch_set(self.root + f"{word}")
        aux_index[word] = dic1.union(aux_index[word])

    def free_aux_index(self, aux_index: dict):
        # free up memory
        for i in range(50):
            word = rnd.choice(list(aux_index.keys()))
            self.dump(aux_index, word)
            aux_index[word] = set([])


if __name__ == '__main__':
    pass

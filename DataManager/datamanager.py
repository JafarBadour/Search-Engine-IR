import os
import os.path
import tarfile
import urllib.request as req


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

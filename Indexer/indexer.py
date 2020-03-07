import re
import unidecode
import json

import nltk
import config

import urllib.request as req
import os.path
import tarfile
from bs4 import BeautifulSoup
import codecs



config.flag = False

# normilize text
def normalize(text, is_query=False):
    text = unidecode.unidecode(text)  # remove accents
    text = re.sub('(\w)', lambda m: m.group(0).lower(), text)  # to_lower the entire text
    if is_query:
        text = re.sub('[^a-z $ *]', "", text)  # remove punctuations
    else:
        text = re.sub('[^a-z ]', "", text)
    text = re.sub('(\ +)', " ", text)  # if we have more than one white space it will become one

    return text


def download_packages():
    if not config.flag:
        print(nltk.download('punkt'))
        nltk.download('stopwords')
        nltk.download('wordnet')
    config.flag = True


def tokenize(text):
    download_packages()
    return nltk.word_tokenize(text)


from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


def lemmatization(tokens):
    lm = WordNetLemmatizer()
    return list(map(lm.lemmatize, tokens))


def stemmatiztion(tokens):
    ps = SnowballStemmer(language='english')
    return list(map(ps.stem, tokens))


def remove_stop_word(tokens):
    stopping_words = set(nltk.corpus.stopwords.words('english'))
    return [word for word in tokens if word not in stopping_words]


def preprocess(text, is_query=False):
    # TODO
    res = remove_stop_word(lemmatization(tokenize(normalize(text,is_query))))
    if not is_query:
        return ["$"+i+"$" for i in res]
    else:
        return res



def download(url, filepath):
    if os.path.isfile(filepath):
        return 0
    else:
        req.urlretrieve(url, filepath)


def get_collection():
    if os.path.isfile('collection.json'):
        with open('collection.json', 'r') as fd:
            return json.load(fd)
    download('https://archive.ics.uci.edu/ml/machine-learning-databases/reuters21578-mld/reuters21578.tar.gz',
             './misc/reuters.tar.gz')
    tf = tarfile.open("./misc/reuters.tar.gz")
    tf.extractall('./misc')
    collection = []
    names = []
    counter = 0
    pattern = re.compile(".+\.sgm$")
    for file in os.listdir("./misc"):
        file = './misc/' + file
        if not pattern.match(file):
            continue
        collection.append([])
        with codecs.open(file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                soup = BeautifulSoup(line)
                collection[-1].extend(preprocess(soup.get_text()))

        print(file)
        names.append(counter)
        counter += 1
    #         if counter == 3:
    #             break

    return [(collection[i], names[i]) for i in range(len(collection))]


def to_n_gram(tokens, n=2):  # default is a bigram
    if type(tokens) != type([]):
        # print(type(tokens))
        tokens = [tokens]
    res = []
    for token in tokens:
        ngrams = zip(*[token[i:] for i in range(n)])
        res += ["".join(ngram) for ngram in ngrams]

    return res


import os.path


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


def make_word_index(collection, force=False):
    inverted_word_index = {}
    ngram_word_index = {}
    if not force:
        a, b = get_cached()
        if bool(a) and bool(b):
            return a, b
    print('gg')
    for (group, name) in collection:
        for word in group:
            if word in inverted_word_index.keys():
                continue
            else:
                ngrams = to_n_gram(word)
                inverted_word_index[word] = ngrams
                for gram in set(ngrams):
                    d = ngram_word_index.setdefault(gram, set([]))
                    d.add(word)
    write_cached(inverted_word_index, ngram_word_index)
    return inverted_word_index, ngram_word_index


def wild_find(token, ngram_word_index):
    temp_token = token
    if len(token) < 2:
        return "Minimum length should be 2 letters"
    if token[-1] == '*':
        token = token[:-1]
        token = "$" + token
    elif token[0] == '*':
        token = token[1:] + "$"
    elif token.find("*") != -1:
        token = token.split('*')
        token[0] = "$" + token[0]
        token[1] = token[1] + "$"

    ngrams = to_n_gram(token)
    # print(ngrams)
    A = ngram_word_index[ngrams[0]]
    temp_token = "\$" + temp_token.replace("*", "[a-z]*") + "\$"
    # print(temp_token)
    pattern = re.compile(temp_token)

    answers = A.intersection(*[ngram_word_index[vi] for vi in ngrams[1:]])
    return [i for i in answers if pattern.match(i)]


import re


def soundex_encode(word):
    assert len(word) > 0, "Word should be non empty"
    dd = {'bfpv': '1', 'cgjkqsxz': '2', 'dt': '3', 'l': '4', 'mn': '5', 'r': '6'}
    d = {}
    for i in dd.keys():
        for j in i:
            d[j] = dd[i]
    word = word[0].upper() + "".join(map(lambda x: d[x], list(re.sub(r'[aeiouhwy]', '', word[1:]))))
    """last = '#'   # ask rustam if slide number 39 makes sense to remove consecutive digits
    nword = ''
    for i in word:
        if i == last:
            continue
        last = i
        nword = nword + i
    word = nword"""
    while len(word) < 4:
        word = word + "0"
    return word[:4]


# %%


def edit_distance(first, second):
    N, M = len(first), len(second)
    dp = [[0 for i in range(M+1) ] for j in range(N+1)]
    for i in range(N+1):
        dp[i][0] = i
    for i in range(M+1):
        dp[0][i] = i
    for i in range(1,N+1,1):
        for j in range(1,M+1,1):
            dp[i][j] = min(dp[i-1][j-1] + (1 if first[i-1] != second[j-1] else 0),dp[i-1][j] + 1, dp[i][j-1]+1)
    return dp[N][M]


def make_index(collection):
    inverted_index = {}
    for (group,name) in collection:
        #print(name)
        for word in group:
            if word in inverted_index.keys():
                inverted_index[word].add(name)
            else:
                inverted_index[word] = set([name])
    return inverted_index


def get_options(token, inverted_word_index, ngram_word_index):
    setty = None
    grams = to_n_gram(token, 2)
    for gram in grams:
        if not setty:
            setty = ngram_word_index[gram]
        setty = setty.union(ngram_word_index[gram])

    mxi, oword = 1000, ''
    arr = []
    for word in setty:
        edit_dst = edit_distance(token, word)
        if edit_dst > 3:
            continue
        arr.append((edit_dst, word))
    arr = sorted(arr)
    # print(arr[:4])
    return [i[1] for i in arr[:5] if i[0] == arr[0][0]]


def correct_spelling(text, inverted_word_index, ngram_word_index):
    tokens = preprocess(text)
    print("query is ", tokens)
    new_text = ""
    for token in tokens:
        options = get_options(token, inverted_word_index, ngram_word_index)
        oword = options[0]
        new_text = new_text + " " + oword

    return new_text


def search(index, query, collection):
    query_copy = preprocess(query, is_query=True)
    expression = ''
    relevant = None
    for word in query_copy:
        potential_words = wild_find(word, ngram_word_index)
        if word.find('*') == -1:
            potential_words = get_options("$" + word + "$", inverted_word_index, ngram_word_index)
        expression = expression + " && (" + " || ".join(potential_words) + ") "

        if not any(word in index for word in potential_words):
            return set()
        new_set = set([])
        new_set = new_set.union(*[index[w] for w in potential_words])  # Union for multiple documents

        if relevant:
            relevant = relevant.intersection(new_set)
        else:
            relevant = new_set
    relevant_documents = [collection[doc_id] for doc_id in relevant]
    print("Query expression is :: ", expression[3:])
    return relevant_documents
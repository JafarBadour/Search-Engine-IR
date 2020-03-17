import functools
import math
import re

import numpy
from sklearn.decomposition import PCA
from System.DataManager.datamanager import tolerant_mkdir, get_parent, save_doc, merge, DBmanager
from System.Parser.query_parser import Parser
import matplotlib.pyplot as plt


def to_n_gram(tokens, n=2):  # default is a bigram
    if type(tokens) != type([]):
        # print(type(tokens))
        tokens = [tokens]
    res = []
    for token in tokens:
        ngrams = zip(*[token[i:] for i in range(n)])
        res += ["".join(ngram) for ngram in ngrams]
    return res


def edit_distance(first, second):
    N, M = len(first), len(second)
    dp = [[0 for i in range(M + 1)] for j in range(N + 1)]
    for i in range(N + 1):
        dp[i][0] = i
    for i in range(M + 1):
        dp[0][i] = i
    for i in range(1, N + 1, 1):
        for j in range(1, M + 1, 1):
            dp[i][j] = min(dp[i - 1][j - 1] + (1 if first[i - 1] != second[j - 1] else 0), dp[i - 1][j] + 1,
                           dp[i][j - 1] + 1)
    return dp[N][M]


def soundex_encode(word):
    assert len(word) > 0, "Word should be non empty"
    dd = {'bfpv': '1', 'cgjkqsxz': '2', 'dt': '3', 'l': '4', 'mn': '5', 'r': '6'}
    d = {}
    for i in dd.keys():
        for j in i:
            d[j] = dd[i]
    word = word[0].upper() + "".join(map(lambda x: d[x], list(re.sub(r'[aeiouhwy]', '', word[1:]))))
    while len(word) < 4:
        word = word + "0"
    return word[:4]


def show_points_2d(X, Y, xaxis, yaxis, paths):
    plt.figure(figsize=(15, 10))
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    classes = set()
    for x, y, p in zip(X, Y, paths):
        plt.plot([x], [y], "o", markersize=20, color='blue')
        plt.text(x, y, p, fontsize=16)
    plt.legend()
    plt.axvline(0)
    plt.axhline(0)
    plt.savefig('../2d.png')
    plt.close()


def show_points_3d(X, Y, Z, paths):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    for x, y, z in zip(X, Y, Z):
        ax.scatter([x], [y], [z], marker='o', color='red')
    plt.savefig('../3d.png')
    plt.close()


def count_tf(tokens):
    res = dict()
    for token in tokens:
        res.setdefault(token, 0)
        res[token] = 1 if not res[token] else res[token] + 1
    for key in res.keys():
        res[key] = res[key]
    return res


def get_matrix(term_doc_index):
    paths = term_doc_index.keys()
    feature_set = set([])
    rows = []
    for path in paths:
        print(term_doc_index[path])
        feature_set.update(term_doc_index[path].keys())
        rows.append(term_doc_index[path])
        if len(feature_set) > 10000:
            break
    s = dict(zip(feature_set, [0] * len(feature_set)))
    res = []
    for row in rows:
        sc = s.copy()
        sc.update(row)
        res.append(list(sc.values()))
    print('Len rows is ', len(rows))

    return res, paths


def get_pca_decomposition(term_doc_matrix):
    A, paths = get_matrix(term_doc_matrix)
    pca = PCA(n_components=3)
    pca.fit(A)
    # print(pca.explained_variance_ratio_)
    k = 3

    Ak = pca.fit_transform(A)
    varience_ratio = pca.explained_variance_ratio_
    print("2 first dimensions")
    show_points_2d(Ak.T[0], Ak.T[1], "1 principal component", "2 principal component", paths)
    print("3 first dimensions")
    show_points_3d(Ak.T[0], Ak.T[1], Ak.T[2], paths)
    return varience_ratio


def retrieve_closest(doc_query_features, docs):
    scores = list(map(lambda x: cosine_similarity(doc_query_features, docs[x]), docs.keys()))
    zipped_doc_score = list(reversed(sorted(zip(scores, docs))))

    scores = list(map(lambda x: x[0], zipped_doc_score))
    docs = list(map(lambda x: x[1], zipped_doc_score))

    return scores, docs


def cosine_similarity(x, y):
    d = {'a': x, 'b': y}
    ar = get_matrix(d)[0]
    return numpy.dot(list(ar[0]), list(ar[1]))


def normalize(term_vector):
    if len(term_vector.keys()) == 0:
        return dict()
    if len(term_vector.keys()) == 1:
        key = list(term_vector.keys())[0]
        term_vector[key] = 1
        return term_vector
    L2norm = math.sqrt(
        functools.reduce(lambda x, y: (term_vector[x] ** 2 if type('str') == type(x) else x) + term_vector[y] ** 2,
                         term_vector.keys()))
    return dict([(i, term_vector[i] / L2norm) for i in term_vector.keys()])


class Indexer:
    def __init__(self):
        self.aux_index = {}
        self.documents = None
        self.collection = None
        self.db = DBmanager()
        self.parser = Parser()
        self.ngram_word_index = {}
        self.term_doc_matrix = dict()
        tolerant_mkdir('.misc')
        tolerant_mkdir('.misc/docs')

    def __call__(self, new_doc):
        path, doc = new_doc

        parent_path = get_parent(path)
        tolerant_mkdir(parent_path)
        save_doc(path, doc)
        collection = self.parser.preprocess(doc)
        zipped_collection = list(zip([path] * len(collection), collection))
        self.fill_term_matrix(path=path, collection=collection)
        self.make_index(zipped_collection)
        self.make_word_index(zipped_collection)
        self.db.free_aux_index(aux_index=self.aux_index)
        # return collection

    def optimize_via_cosine(self, query: str, docs: list):
        if len(docs) == 0:
            return [], []
        tf_vector = normalize(count_tf(self.parser.preprocess(query)))
        print(self.term_doc_matrix.keys())
        docs = dict(map(lambda x:(x, self.term_doc_matrix[x]), docs))
        return retrieve_closest(tf_vector, docs)

    def get_closest_docs(self, doc_query: str):

        doc_query = './' + doc_query
        if not doc_query in self.term_doc_matrix.keys():
            return [None], [f'Incorrect document name {doc_query}']
        doc_query_features = self.term_doc_matrix[doc_query]
        docs = self.term_doc_matrix

        return retrieve_closest(doc_query_features, docs)

    def pca_visualize(self):
        return get_pca_decomposition(self.term_doc_matrix)

    def fill_term_matrix(self, path: str, collection):
        term_vector = normalize(count_tf(collection))
        self.term_doc_matrix.setdefault(path, term_vector)

    def make_word_index(self, collection):
        words = {}
        ngram_word_index = {}

        for path, word in collection:
            if word in words.keys():
                continue
            else:
                words[word] = True
                ngrams = to_n_gram(word)
                for gram in set(ngrams):
                    d = ngram_word_index.setdefault(gram, set([]))
                    d.add(word)
        self.ngram_word_index = merge(self.ngram_word_index, ngram_word_index)

    def make_index(self, collection):
        inverted_index = {}

        for path, word in collection:
            # print(word)
            if word in inverted_index.keys():
                inverted_index[word].add(path)
            else:
                inverted_index[word] = set([path])
        self.aux_index = merge(inverted_index, self.aux_index)

    def wild_find(self, tokens):
        temp_tokens = tokens
        if len(tokens) < 2:
            return "Minimum length should be 2 letters"
        if tokens[-1] == '*':
            tokens = tokens[:-1]
            tokens = "$" + tokens
        elif tokens[0] == '*':
            tokens = tokens[1:] + "$"
        elif tokens.find("*") != -1:
            tokens = tokens.split('*')
            tokens[0] = "$" + tokens[0]
            tokens[1] = tokens[1] + "$"

        ngrams = to_n_gram(tokens)
        if any(not gram in self.ngram_word_index.keys() for gram in ngrams):
            return []
        A = self.ngram_word_index[ngrams[0]]
        temp_tokens = "\$" + temp_tokens.replace("*", "[a-z]*") + "\$"

        pattern = re.compile(temp_tokens)

        answers = A.intersection(*[self.ngram_word_index[vi] for vi in ngrams[1:]])
        return [i for i in answers if pattern.match(i)]

    def get_options(self, token):
        setty = None
        grams = to_n_gram(token, 2)
        for gram in grams:
            if not gram in self.ngram_word_index.keys():
                continue
            if not setty:
                setty = self.ngram_word_index[gram]
            setty = setty.union(self.ngram_word_index[gram])

        arr = []
        if not setty:
            return []
        for word in setty:
            edit_dst = edit_distance(token, word)
            if edit_dst > 3:
                continue
            arr.append((edit_dst, word))
        arr = sorted(arr)
        # print(arr[:4])
        return [i[1] for i in arr[:5] if i[0] == arr[0][0]]

    def correct_spelling(self, text):
        tokens = self.parser.preprocess(text)
        print("query is ", tokens)
        new_text = ""
        for token in tokens:
            options = self.get_options(token)
            oword = token

            if len(options) > 0:
                oword = options[0]

            new_text = new_text + " " + oword

        return new_text

    def search(self, query: str):

        query_copy = self.parser.preprocess(query, is_query=True)
        if len(query_copy) == 0:
            return [], []
        expression = ''
        relevant = None
        for word in query_copy:
            potential_words = self.wild_find(word)
            if word.find('*') == -1:
                potential_words = self.get_options("$" + word + "$")
            expression = expression + " && (" + " || ".join(potential_words) + ") "

            if not any(word in self.aux_index.keys() for word in potential_words):
                return "Nothing", set()
            for wordy in potential_words:
                if len(self.aux_index[wordy]) == 0:
                    print("Retrieving data from db")
                    self.db.update_aux_index(self.aux_index, wordy)
            new_set = set([])
            new_set = new_set.union(*[self.aux_index[w] for w in potential_words])  # Union for multiple documents

            if relevant:
                relevant = relevant.intersection(new_set)
            else:
                relevant = new_set
        relevant_documents = [doc_id for doc_id in relevant]
        print("Query expression is :: ", expression[3:])
        return expression[3:], list(relevant_documents)


if __name__ == '__main__':
    indexer = Indexer()

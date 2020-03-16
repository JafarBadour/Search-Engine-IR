import re
import nltk
import unidecode
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


def normalize(text, is_query=False):
    text = unidecode.unidecode(text)  # remove accents
    text = text.replace('+', ' ')
    text = re.sub('(\w)', lambda m: m.group(0).lower(), text)  # to_lower the entire text
    if is_query:
        text = re.sub('[^a-z $ *]', "", text)  # remove punctuations
    else:
        text = re.sub('[^a-z ]', "", text)
    text = re.sub('(\ +)', " ", text)  # if we have more than one white space it will become one

    return text


def lemmatization(tokens):
    lm = WordNetLemmatizer()
    return list(map(lm.lemmatize, tokens))


def stemmatiztion(tokens):
    ps = SnowballStemmer(language='english')
    return list(map(ps.stem, tokens))


class Parser:
    # normalize text

    def __init__(self):
        self.ntlk_downloaded = False
        self.stopping_words = set(nltk.corpus.stopwords.words('english'))

    def remove_stop_word(self, tokens):

        return [word for word in tokens if word not in self.stopping_words]

    def is_stopping_word(self, token: str):
        return token in self.stopping_words

    def download_packages(self):
        if not self.ntlk_downloaded:
            print(nltk.download('punkt'))
            nltk.download('stopwords')
            nltk.download('wordnet')
        self.ntlk_downloaded = True

    def tokenize(self, text):
        self.download_packages()
        return nltk.word_tokenize(text)

    def preprocess(self, text, is_query=False):

        res = self.remove_stop_word(stemmatiztion(lemmatization(self.tokenize(normalize(text, is_query)))))
        if not is_query:
            return ["$" + i + "$" for i in res]
        else:
            return res

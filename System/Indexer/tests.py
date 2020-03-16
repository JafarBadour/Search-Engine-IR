from System.Indexer.indexer import Indexer

import unittest


class TestIndexer(unittest.TestCase):
    def test_add_document(self):
        document = 'doc'
        path = 'path'
        indexer = Indexer()
        indexer((path, document))
        _, search_path = indexer.search('doc')
        self.assertIn(path, search_path)


if __name__ == '__main__':
    unittest.main()

"""
.assertEqual(a, b)	a == b
.assertTrue(x)	bool(x) is True
.assertFalse(x)	bool(x) is False
.assertIs(a, b)	a is b
.assertIsNone(x)	x is None
.assertIn(a, b)	a in b
.assertIsInstance(a, b)	isinstance(a, b)

"""
#
# #%%
#

#
# #%% md
#
#
# #%%
#

#
# #%% md
#
# #%%
#
# lemmed = lemmatization(tokens)
# print(lemmed)
#
#
# #%%
#
#
# #%%
#
# stemmed = stemmatiztion(tokens)
# print(stemmed)
#
# #%% md
#
#
# #%%
#
# clean = remove_stop_word(stemmed)
# print(clean)
#
# #%% md
#
# #%%
#
#
# clean = preprocess(text)
# print(clean)
#
# #%% md
#
# #%%
#
# collection = get_collection()
#
# print(len(collection))
#
# #%% md
#
# #%%
#
# print(to_n_gram(['$hello$','$ja'],2))
# print(to_n_gram('$hello$',2))
#
#
# #%% md
#
# #%%
#
# #test
#
# print("results for \'h*ell\' are \n",wild_find('h*ell', ngram_word_index))
# print("results for \'j*far\' are \n",wild_find('j*far', ngram_word_index))
# print("results for \'jaafar\' are \n",wild_find('jaafar', ngram_word_index))
#
# print(wild_find('k*', ngram_word_index))
#
#
# #%% md
#
# # test
#
# soundex_encode("Herman")
# #
# #%%
#
# edit_distance('worrld','world')
#
#
# #%% md
#
# #%%
#
# index = make_index(collection)
#
# print(index['$food$'])
#
# #%% md
#
# #%%
#
# correct_spelling('inaguration respctful consititution jafar',inverted_word_index, ngram_word_index)
#
# #%% md
#
# query = 'fanci worrd' # change for something else if you are searching song lyrics
# relevant = search(index, query, collection)
# print("how many relevant docs: ",len(relevant))

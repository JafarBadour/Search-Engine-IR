from Parser.query_parser import Parser, normalize
import unittest

text = """Borrowed from \n\n Latins* $ teachers drunks zinjs per he drank, he killed  he'll  
        \"\"\"\"\'\'   sē (“by itself”), from per (“by, through”) and sē (“itself, himself, herself, themselves”)"""


class TestParser(unittest.TestCase):

    def test_lemmatizer(self):
        result = "borrowed from latins teachers drunks zinjs per he drank " \
                 "he killed hell se by itself from per by through and se itself himself herself themselves"
        parser = Parser()
        temp = normalize(text, False)
        self.assertEqual(result, temp)

    def test_tokenizer(self):
        parser = Parser()

        tokens = parser.tokenize('hello there my name is Morris Moss')
        self.assertEqual(['hello', 'there', 'my', 'name', 'is', 'Morris', 'Moss'], tokens)

    def test_preprocessing(self):
        parser = Parser()
        res = parser.preprocess(text)
        self.assertEqual(
            ['$borrowed$', '$latin$', '$teacher$', '$drunk$', '$zinjs$', '$per$', '$drank$', '$killed$', '$hell$',
             '$se$', '$per$', '$se$'], res)


if __name__ == '__main__':
    unittest.main()

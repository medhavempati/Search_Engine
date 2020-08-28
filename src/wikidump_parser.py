import xml.etree.ElementTree as etree
import os
import time
import pickle
import codecs
import csv
import re
import string
import nltk
from nltk.tokenize import word_tokenize
import time

stopwords = ['r','ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

start_time = time.time()

ENCODING = 'utf-8'

xml_file = './data/enwiki-20200801-pages-articles-multistream1.xml-p1p30303'
# xml_file = './data/test.xml'
articles_file = './articles.csv'
# articles_file = './articles_test.csv'

class Inverted_Index():

    '''
    Indexing mechanism
    0 -> doc
    1 -> field
    2 -> position
    '''

    '''
    Type
    1 - body
    2 - infobox
    3 - references
    4 - outlinks
    5 - sub-headings
    6 - categories
    7 - title
    '''

    def __init__(self):
        self.size = 0
        self.index = {}

    def check(self, check_type, value):
        '''
        Type
        1 -> Word
        2 -> Doc
        '''

        if value == None:
            if check_type == 1:
                print('Error: tried to enter word in index without: word\n')
                exit()
            elif check_type == 2:
                print('Error: tried to enter word in index without: doc_id\n')
                exit()
        return


    def add_new_word(self, word, doc, field=1, pos=0):
        self.check(1, word)
        self.check(2, doc)
        self.index[word] = [[doc, field, pos]]

    def add_to_existing_word(self, word, doc, field=1, pos=0):
        self.check(1, word)
        self.check(2, doc)

        for w in self.index:
            if w == word:
                self.index[word].append([doc, field, pos])

    def find_word(self, word, doc, field=1, pos=0):
        self.check(1, word)
        self.check(2, doc)

        if not bool(self.index):
            self.add_new_word(word, doc, field, pos)


        if word in self.index:
            print(f'found match: {word}')
            self.add_to_existing_word(word, doc, field, pos)
        else:
            print(f'adding new wrod: {word}')
            self.add_new_word(word, doc, field, pos)

        

    def new_article(self, article, doc_id):
        for w in article:
            self.find_word(w, doc_id)

        print(f"index: \n {self.index}")



class Parser():
    def __init__(self):
        self.etree = etree
        self.doc_id = 1
        self.title = ''
        self.article = ''
        self.TEMP = 0
        self.inverted_idx = Inverted_Index()


    def strip_punctuation(self, text):
        intable = '}])([{|":,.=#'
        outtable = '             '
        transtable = str.maketrans(intable, outtable)
        translated_text = text.translate(transtable)
        return translated_text

    def tokenize(self, text):
        text_without_punc = self.strip_punctuation(text)
        tokenized = [w.lower() for w in word_tokenize(text_without_punc)]
        tokens = [w for w in tokenized if not w in stopwords]
        return tokens

    def parse(self):

        # with open('articles_file.csv', 'w') as articlesFH:
        #     articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL)
        #     articlesWriter.writerow(['id', 'title', 'article'])

            for event, element in self.etree.iterparse(xml_file, events=('start', 'end')):
                if self.TEMP == 2:
                    return

                tag = element.tag[43:]
                
                if event == 'end':
                    if tag == 'title':
                        self.title = element.text
                        words_in_title = [w.lower() for w in re.split("([A-Z][^A-Z]*)", self.title) if w]
                        # print(words_in_title)

                        self.TEMP += 1


                    elif tag == 'text':
                        self.article = element.text
                        words_in_article = self.tokenize(self.article)
                        print(words_in_article)
                        self.inverted_idx.new_article(words_in_article, self.doc_id)

                    elif tag == 'page':
                        # articlesWriter.writerow([self.doc_id, self.title, self.article])
                        self.doc_id += 1
                        element.clear()


parser = Parser()
parser.parse()

print(f"time: {time.time()- start_time}")
from dependencies import *

class Inverted_Index():

    '''
    Type
    0 - doc
    1 - body
    2 - infobox
    3 - references
    4 - outlinks
    5 - categories
    6 - title
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

    def new_instance(self, word, doc):
        self.check(1, word)
        self.check(2, doc)
        self.index[word] = [doc, 0, 0, 0, 0, 0, 0]
        

    def add_entry(self, word, doc, field=1):
        self.check(1, word)
        self.check(2, doc)
        self.new_instance(word, doc)
        self.index[word][doc][field] += 1

    def find_word(self, word, doc, field=1):
        self.check(1, word)
        self.check(2, doc)

        if not bool(self.index):
            self.new_instance(word, doc)

        if not word in self.index:
            self.new_instance(word, doc)

        self.add_entry(word, doc, field)

    def new_text(self, article, doc_id, field):
        for w in article:
            self.find_word(w, doc_id)

        # print(f"index: \n {self.index}")
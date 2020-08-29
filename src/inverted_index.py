from dependencies import *

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


    def add_new_word(self, word, doc, field=1):
        self.check(1, word)
        self.check(2, doc)
        matrix = [[]]
        self.index[word] = [[doc[]]]

    def add_to_existing_word(self, word, doc, field=1):
        self.check(1, word)
        self.check(2, doc)

        for w in self.index:
            if w == word:
                self.index[word].append([doc, field, pos])

    def find_word(self, word, doc, field=1):
        self.check(1, word)
        self.check(2, doc)

        if not bool(self.index):
            self.add_new_word(word, doc, field, pos)


        if word in self.index:
            # print(f'found match: {word}')
            self.add_to_existing_word(word, doc, field, pos)
        else:
            # print(f'adding new wrod: {word}')
            self.add_new_word(word, doc, field, pos)

        

    def new_text(self, article, doc_id, field):
        for w in article:
            self.find_word(w, doc_id)

        # print(f"index: \n {self.index}")
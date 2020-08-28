from dependencies import *
from inverted_index import *
from title_log import title_log

start_time = time.time()

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
        tokens = [w for w in tokenized if not w in STOPWORDS]
        return tokens

    def parse(self):

        # with open('articles_file.csv', 'w') as articlesFH:
        #     articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL)
        #     articlesWriter.writerow(['id', 'title', 'article'])

            for event, element in self.etree.iterparse(XML_FILE, events=('start', 'end')):
                if self.TEMP == 2:
                    return

                tag = element.tag[43:]
                
                if event == 'end':
                    if tag == 'title':
                        self.title = element.text
                        words = [w for w in re.split("([A-Z][^A-Z]*)", self.title) if w]
                        title_log[' '.join(words)] = self.doc_id
                        words_in_title = [w.lower() for w in words]
                        self.inverted_idx.new_article(words_in_title, self.doc_id)
                        # print(words_in_title)

                        self.TEMP += 1


                    elif tag == 'text':
                        self.article = element.text
                        words_in_article = self.tokenize(self.article)
                        print(words_in_article)
                        # self.inverted_idx.new_article(words_in_article, self.doc_id)

                    elif tag == 'page':
                        # articlesWriter.writerow([self.doc_id, self.title, self.article])
                        self.doc_id += 1
                        element.clear()


parser = Parser()
parser.parse()
print(title_log)

print(f"time: {time.time()- start_time}")
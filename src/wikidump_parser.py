from dependencies import *
from inverted_index import *
from title_log import title_log

start_time = time.time()

class Parser():
    def __init__(self):
        self.etree = etree
        self.doc_id = 1
        self.TEMP = 0
        self.inverted_idx = Inverted_Index()
        self.body_start = 0
        self.body_end = -1
        self.title = ''


    def strip_punctuation(self, text):
        intable = PUNCTUATION
        outtable = ''                  
        for p in intable:
            outtable += ' '
        transtable = str.maketrans(intable, outtable)
        translated_text = text.translate(transtable)
        return translated_text

    def tokenize(self, text):
        text_without_punc = self.strip_punctuation(text)
        tokenized = [w.lower() for w in word_tokenize(text_without_punc)]
        tokens = [w for w in tokenized if not w in STOPWORDS if not w in ALPHABETS]
        return tokens

    def sent_split(self, text):
        sentences = sent_tokenize(text)
        return sentences

    def parse(self):

        # with open('articles_file.csv', 'w') as articlesFH:
        #     articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL)
        #     articlesWriter.writerow(['id', 'title', 'article'])

            for event, element in self.etree.iterparse(XML_FILE, events=('start', 'end')):
                # if self.TEMP == 13:
                #     return

                tag = element.tag[43:]
                
                if event == 'end':
                    if tag == 'title':
                        self.title = element.text 

                        words = [w for w in re.split("([A-Z][^A-Z]*)", element.text) if w]
                        title_log[' '.join(words)] = self.doc_id
                        words_in_title = [w.lower() for w in words]
                        self.inverted_idx.new_text(words_in_title, self.doc_id, 6)
                        # print(words_in_title)

                        self.TEMP += 1


                    elif tag == 'text':

                        if "Infobox" in element.text:
                            infobox = element.text[element.text.find('Infobox'):]
                            brackets = 2
                            for endpt, char in enumerate(infobox):
                                if char == '{':
                                    brackets += 1
                                if char == '}':
                                    brackets -= 1
                                if brackets == 0:
                                    break
                            infobox_text = infobox[:endpt]
                            self.body_start = endpt+1
                            # print(infobox_text)
                            infobox_lines = infobox_text.split('\n')
                            infobox_text = ''
                            for line in infobox_lines:
                                # print(line)
                                if '=' in line:
                                    infobox_text += line[line.find('='):]
                            # print(infobox_text)
                            infobox_text = self.tokenize(infobox_text)
                            # print(infobox_text)
                            self.inverted_idx.new_text(infobox_text, self.doc_id, 2)
                        else:
                            self.body_start = 0

                        if 'References' in element.text:
                            references = element.text[element.text.find('References'):]
                            self.body_end = element.text.find('References')
                            prev = ''
                            for endpt, char in enumerate(references):
                                if prev == '=' and char == '=':
                                    break
                                prev = char
                            reference_text = references[:endpt-2]
                            reference_lines = reference_text.split('\n')
                            reference_text = ''
                            for line in reference_lines:
                                if '|' in line:
                                    reference_text += line[line.find('|'):]
                            reference_text = self.tokenize(reference_text)
                            self.inverted_idx.new_text(reference_text, self.doc_id, 3)


                        start_idx = None
                        if '==External' in element.text:
                            start_idx = element.text.find('==External')
                        elif '== External' in element.text:
                            start_idx = element.text.find('== External')
                        elif '==Links' in element.text:
                            start_idx = element.text.find('==Links')
                        
                        if '[[Category' in element.text:
                            end_idx = element.text.find('[[Category')
                        else:
                            end_idx = -1

                        if start_idx != None:
                            links_text = element.text[start_idx:end_idx]
                            links_text = self.tokenize(links_text)
                            self.inverted_idx.new_text(links_text, self.doc_id, 4)

                            if self.body_end == -1:
                                self.body_end = start_idx



                        if '[[Category' in element.text:
                            category_text = element.text[element.text.find('[[Category'):]
                            if self.body_end == -1:
                                self.body_end = element.text.find('[[Category')
                            category_lines = category_text.split('\n')
                            # print(category_lines) 

                            category_text = ''
                            for line in category_lines:
                                category_text += ' ' + line[line.find(':')+1:line.find(']')]
                            # print(f'\n\nCATEGORY TEXT: {category_text}\n\n')
                            category_text = self.tokenize(category_text)
                            
                            self.inverted_idx.new_text(category_text, self.doc_id, 5)

                        body_text = element.text[self.body_start:self.body_end]
                        body_text = self.tokenize(body_text)
                        # print(words_in_article)
                        self.inverted_idx.new_text(body_text, self.doc_id, 1)

                    elif tag == 'page':
                        # articlesWriter.writerow([self.doc_id, self.title, self.article])
                        print(f'{self.title}\n')
                        self.doc_id += 1
                        element.clear()


parser = Parser()
parser.parse()
# print(title_log)
# print(f'index:\n {parser.inverted_idx.index}')

print(f"time: {time.time()- start_time}")
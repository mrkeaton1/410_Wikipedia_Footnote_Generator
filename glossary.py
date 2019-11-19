from format_pdf import PDF
import wikisearch as wiki
from nltk import word_tokenize, sent_tokenize
import itertools
import re
import argparse
import requests
import unicodedata
from collections import OrderedDict

def unicode_normalize(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
        
class unique_words(OrderedDict):
    def __missing__(self, key):
        return None

def parse_tokens(input_txt):
    #get the unicode into ascii to save headaches with pdf generation
    input_txt = unicode_normalize(input_txt)
    
    #get and preserve paragraphs
    paras = re.split("(\n\s*\n)", input_txt.decode('ASCII'))
    sents_by_para = [sent_tokenize(p) for p in paras ]

    #the input text is parsed and tokenized.
    # We keep the whitespaces, for purposes of formatting.
    parsed_txt = []
    for para in sents_by_para:
        if bool(para):
            for sent in para:
                ll = [[word_tokenize(w), ' '] for w in sent.split()]
                parsed_txt.extend(list(itertools.chain(*list(itertools.chain(*ll)))))
        else:
            parsed_txt.extend('\n\n')
    
    return parsed_txt

######################### Main Code #############################
######### Setup the command line arguments ########

parser = argparse.ArgumentParser(description='Generate a linked glossary PDF of input text')

parser.add_argument('--infile', metavar='<filename|URL>', required=True,
                    help='The file to be processed. Can be a URL.')
parser.add_argument('--outfile', metavar='[filename]',
                    default="annotated.pdf",
                    help='The name of the file to output to.')
parser.add_argument('--title', metavar='<Title>', required=True,
                    default="annotated",
                    help='The title of the text file.')
parser.add_argument('--common', default=None,
                    help='an external stopword list. Default will use nltk.')

args = parser.parse_args()

########## Parse the text #########################
parsed_txt = ""
word_dictionary = unique_words()

#### Get the text into token format. #####
if re.match("^https?://", args.infile):
    r = requests.get(args.infile, allow_redirects=True)
    parsed_txt = parse_tokens(r.text)
else:
    with open(args.infile, 'r') as input_file:
        input_txt = input_file.read()
        parsed_txt = parse_tokens(input_txt)

with open("testfile.txt", 'w') as test:
    for string in parsed_txt:
        test.write(str(string))
        
common_words = []
    ### use a local list of common words, or the nltk stopwords ###
if args.common:
    with open(args.common, 'r') as common:
        common_words = [line.rstrip('\n') for line in common]
        common_words.append(["\n","thee","thy","ye","thine","thou"])
else:
    #get stopwords + extra for the era of the book at the url
    from nltk.corpus import stopwords
    common_words = stopwords.words('english')
    extrastop = ["thee", "thy", "ye", "thine", "thou","\n"]
    common_words.append(extrastop)

########## Get the unique words and their position. ######
visited = []
indexes = []
for idx, token in enumerate(parsed_txt):
    
    
    #put this in our dictionary, if not in it already, and not common.
    if token.lower() not in visited:
        if token.lower() not in common_words:
            word_dictionary[token] = idx
            visited.append(token.lower())

######### Get the glossary entries ##############
notes = wiki.note_generator(word_dictionary)

############## Create PDF ###############
pdf = PDF()
pdf.set_title(args.title)
pdf.set_left_margin(10)
pdf.set_right_margin(10)
pdf.print_document(parsed_txt, word_dictionary, notes)
pdf.output(args.outfile, 'F')

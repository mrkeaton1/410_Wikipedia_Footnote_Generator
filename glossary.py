from format_pdf import PDF
import wikisearch as wiki
from nltk import word_tokenize, sent_tokenize
import itertools
import re
import argparse

class unique_words(dict):
    def __missing__(self, key):
        return None

def parse_tokens(input_txt):
    #get and preserve paragraphs
    paras = re.split("(\n\s*\n)", input_txt)
    sents_by_para = [ sent_tokenize(p) for p in paras ]

    #the input text is parsed and tokenized. Where there is a unique word,
    #the text is altered with some hypertext to indicate a key word.
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

parser.add_argument('--infile', metavar='<filename>', required=True,
                    help='The file to be processed')
parser.add_argument('--outfile', metavar='[filename]', required=True,
                    default="annotated.pdf",
                    help='The name of the file to output to.')
parser.add_argument('--title', metavar='<Title>', required=True,
                    default="annotated",
                    help='The title of the text file.')

args = parser.parse_args()

########## Parse the text #########################
parsed_txt = ""
word_dictionary = unique_words()

#### Get the text into token format. #####
with open(args.infile, 'r') as input_file:
    input_txt = input_file.read()
    parsed_txt = parse_tokens(input_txt)

common_words = []
with open('common.txt', 'r') as common:
    common_words = [line.rstrip('\n') for line in common]
    common_words.append('\n')
    #print(common_words)

########## Get the unique words and their position. ######
for idx, token in enumerate(parsed_txt):
    
    #put this in our dictionary, if not in it already, and not common.
    if type(word_dictionary[token.lower()]) is not str:
        if token.lower() not in common_words:
            word_dictionary[token] = idx

######### Get the glossary entries ##############
notes = wiki.note_generator(word_dictionary)

############## Create PDF ###############
pdf = PDF()
pdf.set_title(args.title)
pdf.set_left_margin(10)
pdf.set_right_margin(10)
pdf.print_document(parsed_txt, word_dictionary, notes)
pdf.output(args.outfile, 'F')

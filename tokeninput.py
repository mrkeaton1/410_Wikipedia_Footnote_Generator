from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
import urllib2
import string

#reads from the file defined in project specs on ecampus
url = "http://www.gutenberg.org/cache/epub/9845/pg9845.txt"
response = urllib2.urlopen(url)
raw = response.read().decode('utf8')
# alternate:
# raw = "your string here" or read in a txt file 

#tokenize to keep only words
tokenizer = RegexpTokenizer(r'\w+')
nopunct = tokenizer.tokenize(raw)

#get stopwords + extra for the era of the book at the url
stopwords = stopwords.words('english')
extrastop = ["thee", "thy", "ye", "thine", "thou"]
stopwords.append(extrastop)
nostop = [w for w in nopunct if not w in stopwords]

#remove repeats
norepeat = list(set(nostop))
#add all of the words + their initial location to a dictionary
dictionary = {}
for w in norepeat:
    dictionary[w.upper().encode('utf8')] = raw.find(w)

#write to file
with open('tokens.txt', 'w') as file:
    file.write(str(dictionary))

# 410_Wikipedia_Footnote_Generator - GlossyText
This project was created to generate a glossary that will provide a summary of unfamiliar or uncommon words based on Wikipedia entries and include a link to the Wikipedia page.

## Running the program
In order to run this program, you call it at the commandline with four arguments: the input file(either a local .txt file or a link to an online .txt file), the output file, the (optional) stopword/common word file, and the title of the work. A few examples are provided below.

### Examples
python3 glossary.py --infile="http://www.gutenberg.org/cache/epub/9845/pg9845.txt" --outfile="gutenout.pdf" --title="Gutenberg Text" --common="106k-combine.txt"

python3 glossary.py --infile="https://www.gutenberg.org/ebooks/60718.txt.utf-8" --outfile="animals.pdf" --title="Living Animals of the World" --common="106k-combine.txt"

python3 glossary.py --infile="coal.txt" --outfile="coalout.pdf" --title="Coal" --common="106k-combine.txt"

### Required software/packages
Make sure this is run on a Linux machine.
Python 3 and the standard libraries must be downloaded, as well as the following packages:
- nltk
- wikipedia
- fpdf

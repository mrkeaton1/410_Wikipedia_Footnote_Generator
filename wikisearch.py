import wikipedia

def note_generator(word_dictionary):
    '''This function will take a unique word dictionary and return
    a list of tuples of the form ('word','first sentence','hyperlink').
    '''
    note_list = []
    for word, index in word_dictionary.items():
        
        #look up and get first sentence and a hyperlink. Make a note.
        sent, link = wiki_lookup(word)
        note = (word,sent,link)
        
        #add the note to the list
        note_list.append(note)
    
    return note_list

def wiki_lookup(word):
    try:
        sent = wikipedia.summary(word, sentences = 1)
        link = wikipedia.page(word).url
    except wikipedia.exceptions.DisambiguationError:
        sent = 'Page not found in Wikipedia. Try the following link for more information:'
        link = "https://duckduckgo.com/?q={}&t=canonical&ia=web".format(word)
    except wikipedia.exceptions.PageError:
        sent = 'Page not found in Wikipedia. Try the following link for more information:'
        link = "https://duckduckgo.com/?q={}&t=canonical&ia=web".format(word)
    
    return sent, link

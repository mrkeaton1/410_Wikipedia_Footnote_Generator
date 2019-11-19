#import wiki module here

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
    #do your magic wiki stuff here, puttin the first sentence in sent
    sent = "Definition would be here"
    
    #put the page link in link. If can't find page, maybe using a search
    #like this below would be a good default? Perhaps search wiki.
    link = "https://duckduckgo.com/?q={}&t=canonical&ia=web".format(word)
    
    return sent, link

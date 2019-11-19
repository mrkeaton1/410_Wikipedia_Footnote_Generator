from fpdf import FPDF, HTMLMixin
import unicodedata

class PDF(FPDF, HTMLMixin):
    def __init__(self):
        FPDF.__init__(self)
        HTMLMixin.__init__(self)
        self.add_font('DejaVu', '', 'DejaVuSerif.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'DejaVuSerif-Bold.ttf', uni=True)
        self.add_font('DejaVu', 'I', 'DejaVuSerif-Italic.ttf', uni=True)
        self.set_font('DejaVu', '', 15)
        
    def header(self):
        # Arial bold 15
        self.set_font('DejaVu', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(self.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, self.title, align='C')
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('DejaVu', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10,'Page ' + str(self.page_no()), 0, 0, 'C')

    def text_body(self, all_words, key_words):
        link_list = []
        # Times 12
        self.set_font('DejaVu', '', 12)
        
        # Output text, bolding the keywords, and creating a link.
        for value, word in enumerate(all_words):
            
            #manually reseting the abscissa .. dirty I know
            if self.get_x() + self.get_string_width(str(word)) > 200:
                self.ln()
                
            if key_words[word] == value:   #if exists, and is first occurance
                self.set_font('DejaVu','B', 12)
                
                #create the link...
                link = self.add_link()
                
                #add a link here. Will be set later.
                link_list.append(link)
                w = self.get_string_width(str(word))
                self.cell(w,5,str(word),ln=0,link=link)
            else:
                #nothing special here.
                self.set_font('')
                w = self.get_string_width(str(word))
                if str(word) == "\n":
                    self.ln()
                else:
                    self.cell(w,5,str(word),ln=0)
        
        # Line break
        self.ln()
        
        # Draw line for the end of the input text
        self.line(0, self.get_y(), 210, self.get_y())
        
        return link_list
    
    def text_glossary(self, notes, links):
        
        for idx, note in enumerate(notes):
            
            #get the parts of the entry
            word, sentence, hyperlink = note
            
            #set the keyword link from the text to this entry.
            self.set_link(links[idx],y=-1,page=-1)
            #print the entry word.
            self.ln()
            self.ln()
            self.set_font('DejaVu','I',12)
            self.cell(0,5,str(word),ln=1)
            
            #print the first sentence entry of the word.
            self.set_font('')
            self.cell(0,5,str(sentence), ln=1)
            
            #print the hyperlink to the wikipedia page.
            self.set_font('DejaVu','U',12)
            self.write_html("""<A href="{0}">{0}</A>\n""".format(hyperlink))

    def print_document(self, all_words, key_words, notes):
        self.add_page()
        link_list = self.text_body(all_words, key_words)
        self.add_page()
        self.text_glossary(notes, link_list)

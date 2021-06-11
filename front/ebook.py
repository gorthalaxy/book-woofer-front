from ebooklib import epub
from bs4 import BeautifulSoup

class KindleText():
    """
    Input :  Path to a kindle epub file
    Output : Python text
    """
    def __init__(self, epub_path):
        self.epub_path = epub_path
        self.blacklist = ['[document]','noscript', 'header',
                          'html', 'meta', 'head','input', 'script']
    def epub2thtml(self):
        book = epub.read_epub(self.epub_path)
        chapters = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters.append(item.get_content())
        return chapters
    def chap2text(chap):
        output = ''
        soup = BeautifulSoup(chap, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
        return output
    def thtml2ttext(thtml):
        Output = []
        for html in thtml:
            text =  chap2text(html)
            Output.append(text)
        return Output
    def epub2text(self,):
        """
        Final function to output the text
        """
        chapters = epub2thtml(self.epub_path)
        ttext = thtml2ttext(chapters)
        return ttext
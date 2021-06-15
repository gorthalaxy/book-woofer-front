from ebooklib import epub
from bs4 import BeautifulSoup

def chap2text(chap):
    blacklist = ['[document]', 'noscript', 'header',
                 'html', 'meta', 'head', 'input', 'script']
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def read_book(temporary_location):
  book = epub.read_epub(temporary_location)
  chapters = []
  for item in book.get_items():
    if str(type(item)) == "<class 'ebooklib.epub.EpubHtml'>":
      chapters.append(item.get_content())
  Output = []
  for html in chapters:
      text = chap2text(html)
      Output.append(text)
  return Output
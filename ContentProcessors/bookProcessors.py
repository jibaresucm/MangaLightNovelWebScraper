from bs4 import BeautifulSoup
from ContentProcessors.processor import Processor
from ContentProcessors.processedData import ProcessedData
from Database.contentRequest import ContentRequest
#Cases wto parse chapters: chapters.size = 0, no nextButton, all chapters in 1 page, all chapters after 1 load more click, api requests

#Use the urls to fetch the chapter (page prefix and suffix) when possible
#Next option is apiCalls

#Returns a list of the links to all the chapters of a book
class BookConfiguration():
    def __init__(self, name, synopsis, parent_url, content, save_path):
        self.name = name
        self.synopsis = synopsis
        self.parent_url = parent_url
        self.content = content
        self.save_path = save_path

class BookProcessor(Processor):

    def __init__(self, info_container, preppend_to_url, append_to_url, chapter_type, title_selector, synopsis_selector):
        super().__init__()
        self.preppend_to_url = preppend_to_url
        self.append_to_url = append_to_url
        self.chapter_type = chapter_type
        self.info_container = info_container
        self.title_selector = title_selector
        self.synopsis_selector = synopsis_selector

class StandardBookProcessor(BookProcessor):
    def process(self, content):
        #Add error checking and save at least the name of the book

        pagesoup = BeautifulSoup(content.data, "html.parser")
        if not pagesoup: return -1

        chaptersoup = pagesoup.select_one(self.info_container)
        if not chaptersoup: return -1

        title = pagesoup.select_one(self.title_selector)
        if not title: return -1
        title = cleanString(title.get_text())

        synopsis = pagesoup.select_one(self.synopsis_selector)
        if synopsis:
            synopsis = cleanString(synopsis.get_text())
        else: synopsis = ""

        chaptersoup = chaptersoup.find_all("a")
        if not chaptersoup: return -1
                
        chapters = []
        for c in chaptersoup:
            chapters.append(ContentRequest(self.preppend_to_url + c['href'] + self.append_to_url, content.parent_url, self.chapter_type,"", content.save_path + "/" + cleanString(c.get_text()) + ".txt"))
        
        ret = ProcessedData("save_n_fetch", chapters, BookConfiguration(title, synopsis, content.parent_url, "BookConf", content.save_path + "/" + title), "test")
        return ret

def cleanString(title: str) -> str:
    ret = ""
    reached = False
    previousSpace = False
    for elem in title:
        if not reached and (elem != ' ' and elem != '\n'): reached = True

        if reached and elem != '\n' and elem != ' ': 
            if previousSpace:
                ret += ' ' + elem
            else:
                ret += elem

            previousSpace = False

        if reached and (elem == ' ' or elem == '\n'): previousSpace = True
        
    return ret




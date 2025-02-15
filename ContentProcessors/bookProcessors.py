from bs4 import BeautifulSoup
from processor import Processor
from processedData import ProcessedData
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

    def __init__(self, info_container, preppend_to_url, chapter_type, append_to_url):
        super().__init__()
        self.preppend_to_url = preppend_to_url
        self.append_to_url = append_to_url
        self.chapter_type = chapter_type
        self.info_container = info_container

class StandardBookProcessor(BookProcessor):
    def process(self, content):
        #Add error checking and save at least the name of the book

        pagesoup = BeautifulSoup(content.data, "html.parser")
        if not pagesoup: return

        chaptersoup = pagesoup.select_one(self.info_container)
        if not chaptersoup: return

        chaptersoup = chaptersoup.find_all("a")
        if not chaptersoup: return
                
        chapters = []
        for c in chaptersoup:
            chapters.append(ContentRequest(self.preppend_to_url + c['href'] + self.append_to_url, content.parent_url, self.chapter_type,"", content.save_path + "/" +c.get_text()))
        
        ret = ProcessedData("save_n_fetch", chapters)
        return chapters





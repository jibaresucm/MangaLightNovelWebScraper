from bs4 import BeautifulSoup
from ContentProcessors.processor import Processor
from ContentProcessors.processedData import ProcessedData
from Database.contentRequest import ContentRequest

class Website():
    def __init__(self, save_path):
        self.content = "WebsiteConf"
        self.save_path = save_path

class BookWebsiteProcessor(Processor):
    def __init__(self,book_container, append_to_url, a_book_href_selector):
        super().__init__()
        self.book_container = book_container
        self.a_book_href_selector = a_book_href_selector
        self.append_to_url = append_to_url

class StandardWebsiteProcessor(BookWebsiteProcessor):
    def process(self, content):
        pagesoup = BeautifulSoup(content.data, "html.parser")
        if not pagesoup: return -1

        book_list = pagesoup.select_one(self.book_container)
        if not book_list: return -1


        book_list = book_list.select("h3.novel-title")
        if not book_list: return -1
        content_request_list = []
        for elem in book_list:
            elem = elem.select_one("a")
            content_request_list.append(ContentRequest(elem["href"] + self.append_to_url, content.parent_url, "book", "", content.save_path))
            
        return ProcessedData("save_n_fetch", content_request_list, Website(content.save_path))
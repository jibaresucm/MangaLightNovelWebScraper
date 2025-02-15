
class WebsiteConf():

    #Saves the css ids to identify the elements, type of content ,parent url etc..
    def __init__(self, parent_url, chapter_type, books_url, website_fetch_option, book_fetch_option, chapter_fetch_option, website_process_handler, book_process_handler, chapter_process_handler):
        self.parent_url = parent_url
        self.chapter_type = chapter_type
        self.books_url = books_url

        self.fetchOptions = {"website": website_fetch_option, "book": book_fetch_option, "chapter": chapter_fetch_option}
        self.processorHandlers = {"website": website_process_handler, "book": book_process_handler, "chapter": chapter_process_handler}

    #Starts the fetching process by adding a content request of the book_url to the database
    def fetchAllContent(self):
        pass

    def getParentUrl(self):
        return self.parent_url
    
    def getProcessorHandlerFor(self, content_type):
        return self.processorHandlers[content_type]
    
    def getFetchOptionFor(self, content_type):
        return self.fetchOptions[content_type]
    
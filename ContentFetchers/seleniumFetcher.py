from selenium import webdriver
import asyncio
import time
from Database.contentRequest import ContentRequest
from ContentFetchers.contentResponse import ContentResponse

class SeleniumFetcher():
    max_webdrivers = 1
    webdrivers = []
    request_list = []

    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        

        for _ in range(self.max_webdrivers):
             self.webdrivers.append(webdriver.Chrome(options=options))
        
        pass
    
    def addRequest(self, req):
        self.request_list.append(req)

    #Limit to max_webdrivers with a infinite amout of toFetchUrls, do not use coroutines since the are executend in a single thread and therefore not optimal becouse 
    #of context chnange and the fact that we are most of the time not "waiting" but processing the visuals

    async def getRequests(self):
        req_size = len(self.request_list)
        all_responses = []

        subSetUrls = []
        count = 0
        tasks = []
        for elem in self.request_list:
            subSetUrls.append(elem)
            tasks.append(self.fetchSingle(self.webdrivers[count % self.max_webdrivers], elem))
            count += 1
            if(count % self.max_webdrivers == 0 or count == req_size):

                responses = await asyncio.gather(*tasks)

                for elem in responses:
                    all_responses.append(elem)
                
                subSetUrls.clear()
                tasks.clear()

        self.request_list.clear()
        return all_responses

    #Use the extra data to take in more steps like waiting 3 seconds or pressing some buttons and return a list always
    async def fetchSingle(self, webdriver: webdriver.Chrome, req : ContentRequest) -> ContentResponse:
        webdriver.get(req.url)
        return ContentResponse(req.url, req.parent_url, req.content_type, req.save_path, webdriver.page_source, True)


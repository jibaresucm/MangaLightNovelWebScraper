from selenium import webdriver
import asyncio
import time

class SeleniumFetcher():
    max_webdrivers = 5
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

    #TODO rethink this for contentRequests not urls
    async def getRequests(self):
        start = time.time()
        urls_size = len(self.url_list)
        print(f"Trying to fetch {urls_size} urls")
        all_responses = []

        subSetUrls = []
        count = 0
        tasks = []
        for elem in self.request_list:
            subSetUrls.append(elem)
            tasks.append(self.fetchSingle(self.webdrivers[count % self.max_webdrivers], elem))
            count += 1
            if(count % self.max_webdrivers == 0 or count == urls_size):

                responses = await asyncio.gather(*tasks)

                for elem in responses:
                    all_responses.append(elem)
                
                subSetUrls.clear()
                tasks.clear()
        print(f"{time.time() - start}s")

        self.url_list.clear()
        return all_responses

    #Use the extra data to take in more steps like waiting 3 seconds or pressing some buttons and return a list always
    async def fetchSingle(self, webdriver: webdriver.Chrome, url):
        webdriver.get(url)
        return webdriver.page_source


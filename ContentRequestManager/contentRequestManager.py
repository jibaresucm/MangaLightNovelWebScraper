from Database.contentRequestDAO import ContentRequestDAO
from ContentFetchers.contentResponse import ContentResponse

class ContentRequestManager():

    def __init__(self,fetchersDictionary: dict, processorsDictionary: dict, websiteDictionary: dict):
        self.fetchersDictionary =  fetchersDictionary
        self.processorsDictionary =  processorsDictionary
        self.websiteDictionary =  websiteDictionary
        self.databaseDAO = ContentRequestDAO()
        self.fetchingRequirements = {}

    #Function to handle content
    def handleContentRequests(self):
        #Get from db uncompleted
        uncompleted_requests = self.databaseDAO.getContentRequests()

        #Fetch
        #We look for a websiteConf that matches the parent url of the request to get the method of the fetching
        for elem in uncompleted_requests:
            self.fetchersDictionary[self.websiteDictionary[elem.parent_url].getFetchOptionFor(elem.content_type)].addRequest(elem)
        
        #Launch the fetching threads TODO (getRequests in fetchersDictionary)
        response_list = []
        
        for elem in self.fetchersDictionary:
            pass #Launch getRequests for each fetcher and save in response_list
        
        #Process functions should return content or a list of urls to fetch later
        #Return an image/text in case of content
        #Return a list of url of chapters or mangas in case of book/website
        #Each content request should have its path if path is null it means that it is the first
        #Process handlers are classes that execute a script specific to the website and contain all the css descriptors of the data
        elem = ContentResponse()
        processed_data = []
        for a in response_list:
            if(elem.successful):
                try:
                    processed_data.append(self.websiteDictionary[elem.parent_url].getProcessorHandlerFor(elem.content_type).process(elem.data))
                except:
                  processed_data.append(-1)  
            else:
                processed_data.append(-1)
            #Else set in db as request failed and notify also do try catch in process() to catch exceptions if an exception is catched set as failed in db and notify
        
        for res, data in response_list, processed_data:
            pass #Add new requests in db with previous content_request info or save the data in storage system
        

        #Process fetched data
        #Save fetched data or add new requests

        #Handle fetch errors (observer)
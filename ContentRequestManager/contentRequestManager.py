from Database.contentRequestDAO import ContentRequestDAO
from ContentFetchers.contentResponse import ContentResponse
from ContentProcessors.processedData import ProcessedData
import os
import asyncio

class ContentRequestManager():

    def __init__(self,fetchersDictionary: dict, websiteDictionary: dict):
        self.fetchersDictionary =  fetchersDictionary

        self.websiteDictionary =  websiteDictionary
        self.databaseDAO = ContentRequestDAO()

    #Function to get process and handle contentRequests and its responses
    async def handleContentRequests(self):
        #Get from db uncompleted
        uncompleted_requests = self.databaseDAO.getContentRequests()

        self.distributeRequestsToFetchers()
        
        response_list = await self.getResponseList()

        processed_data = self.processResponses(response_list)
        
        self.handleProcessedData(processed_data)

    #Adds the content requests to its corresponding fetcher looking for the configuration in the websiteConf dict
    def distributeRequestsToFetchers(self, uncompleted_requests):
        for elem in uncompleted_requests:
            self.fetchersDictionary[self.websiteDictionary[elem.parent_url].getFetchOptionFor(elem.content_type)].addRequest(elem)

    #Launches the fetchers and gets the responses, it puts them all in a list
    async def getResponseList(self)-> list:
        response_list = []
        
        for elem in self.fetchersDictionary.values():
            responses = await elem.getRequests()
            for response in responses:
                response_list.append(response)
        return response_list

    #With the responses already fetched we extract the valuable info of the html and return it
    def processResponses(self, response_list: list)-> list:
        processed_data = []
        for elem in response_list:
            if(elem.successful):
                try:
                    processed_data.append(self.websiteDictionary[elem.parent_url].getProcessorHandlerFor(elem.content_type).process(elem))
                    self.databaseDAO.setAsComplete(elem.url)
                except:
                    self.databaseDAO.setAsFailed(elem.url)
            else:
                self.databaseDAO.setAsFailed(elem.url)
        return processed_data

    #With the processed data we save the information, save content requests to the database to be launched later and make directories to prepare for arrival of info
    def handleProcessedData(self, processed_data: ProcessedData):
        for data in processed_data:
            if(data.action == "save_n_fetch"):
                self.addToFetch(data.fetch_list)
                self.saveData(data.save_data)
                pass
            elif (data.action == "fetch"):
                self.addToFetch(data.fetch_list)
                pass
            elif(data.action == "save"):
                self.saveData(processed_data.save_data)
                pass

    def saveData(self, elem):
        match elem.content:
            case "BookConf":
                self.createDir
                self.saveBook(elem)
    
    def saveBook(self, obj):
        with open("." + obj.save_path+ "/data.txt", "w", encoding="UTF-8")as fd:
            fd.write(obj.name+ '\n')
    
    def createDir(self, obj):
        try:
            os.mkdir("." + obj.save_path)
        except Exception as e:
            pass

    def addToFetch(self, new_request_list: list):
        for elem in new_request_list:
            try:
                self.databaseDAO.addContentRequestEntry(elem)
            except Exception as e:
                pass

import unittest
import asyncio
from ContentProcessors.bookProcessors import StandardBookProcessor
from ContentRequestManager.contentRequestManager import ContentRequestManager
from WebsiteConfigurations.websiteConf import WebsiteConf
from ContentFetchers.httpFetcher import HttpFetcher
from ContentFetchers.seleniumFetcher import SeleniumFetcher
from ContentProcessors.bookProcessors import StandardBookProcessor
from Database.contentRequest import ContentRequest


class TestContentRequestManager(unittest.TestCase):

    def test_realtest(self):
        asyncio.run(self.getRequest())

    async def getRequest(self):
        sel = SeleniumFetcher()
        sel.addRequest(ContentRequest("https://novelbin.com/b/isekai-nonbiri-nouka", "https://novelbin.com", "book", "Unrequested", "/ContentRequestManager/tests/TestData"))
        fetchersDict = {"selenium": sel, "http": HttpFetcher()}
        websiteDict = {"https://novelbin.com": WebsiteConf("https://novelbin.com", "", "", "selenium", "selenium", "http", "", StandardBookProcessor("#list-chapter","","","text", ".title","ul.info-meta.info"), "")}

        rm = ContentRequestManager(fetchersDict, websiteDict)
        
        response_list = await rm.getResponseList()

        processed_data = rm.processResponses(response_list)
        
        rm.handleProcessedData(processed_data)
        

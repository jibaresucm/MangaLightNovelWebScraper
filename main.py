from WebsiteConfigurations.websiteConf import WebsiteConf
from ContentFetchers.httpFetcher import HttpFetcher
from ContentFetchers.seleniumFetcher import SeleniumFetcher
from ContentRequestManager.contentRequestManager import ContentRequestManager
from ContentProcessors.bookProcessors import *
from ContentProcessors.websiteProcessors import *
from ContentProcessors.chapterProcessors import *
import time
import asyncio


sel = SeleniumFetcher()
http = HttpFetcher()
fetchersDict = {"selenium": sel, "http": http}
#sel.addRequest(ContentRequest("https://novelbin.com/sort/top-hot-novel", "https://novelbin.com", "website", "", "/Novelbin"))
#sel.addRequest(ContentRequest("https://novelbin.com/b/isekai-nonbiri-nouka", "https://novelbin.com", "book", "Unrequested", "/Novelbin"))
websiteDict = {"https://novelbin.com": WebsiteConf("https://novelbin.com", "", "", "selenium", "selenium", "http", StandardWebsiteProcessor("div.list.list-novel", "#tab-chapters-title", "h3.novel-title.a"), StandardBookProcessor("#list-chapter","","","text", ".title","ul.info-meta.info"), TextChapterProcessor("#chr-content"))}

rm = ContentRequestManager(fetchersDict, websiteDict)

for elem in range(10):
    asyncio.run(rm.handleContentRequests())
    time.sleep(3)


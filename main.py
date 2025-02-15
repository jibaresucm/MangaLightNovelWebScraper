from WebsiteConfigurations.websiteConf import WebsiteConf

websiteConfList = [WebsiteConf("https://parent_url.com")]

websiteHashMap = {}
for elem in websiteConfList:
    websiteHashMap[elem.getParentUrl()] = elem

for elem in websiteHashMap:
    #Adds entry to contentRequests  with options
    pass

#Starts contentRequestManager (Module in charge of feeding the requests from the database to the fetchers. It also processes the data after the response arrives adding the pertinent request
#when necessary)

#Http fetcher takes all the requests and sends them, seleniumFetcher since it is not a requests api needs to work differently.
#Selenium fetcher uses the selenium browser to get in other cases unaccesible data
#It deploys a n number of browsers and uses them to get the request in a similar fashion to to the http fetcher


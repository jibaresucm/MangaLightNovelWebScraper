#Module where the webbrowser and request get the html page sources
#The purpose of it is to do it in an async way
#We can use a sql database with chapter requests table and

#https requests -> url, type="text_chapter, image_chapter, chapters, books", websiteurl, 
#selenium requests -> url

#Website conf objects that stores its website

import aiohttp
import asyncio



class HttpFetcher():

    request_list = []
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Ch-Ua":'"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Cache-Control": "max-age=0",
            "Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
            "Sec-Ch-Ua-platform":'"Windows"'
            }

    async def getRequests(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetchSingle(session, currUrl) for currUrl in self.request_list]
            responses = await asyncio.gather(*tasks)
            self.request_list.clear()
            return responses

    def addRequest(self, url):
        self.request_list.append(url)

    async def fetchSingle(self, session: aiohttp.ClientSession, url):
        async with session.get(url, headers=self.headers ) as response:

            if(response.status == 200):
                return await response.text()
            else: 
                return -1

#asyncio.get_event_loop().run_until_complete()
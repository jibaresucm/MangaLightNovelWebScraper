import aiohttp
import asyncio
from Database.contentRequest import ContentRequest
from ContentFetchers.contentResponse import ContentResponse



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
            tasks = [self.fetchSingle(session, req) for req in self.request_list]
            responses = await asyncio.gather(*tasks)
            self.request_list.clear()
            return responses

    def addRequest(self, req :ContentRequest):
        self.request_list.append(req)

    async def fetchSingle(self, session: aiohttp.ClientSession, req:ContentRequest)-> ContentRequest:
        async with session.get(req.url, headers=self.headers ) as response:

            if(response.status == 200):
                return ContentResponse(req.url, req.parent_url, req.content_type, req.save_path, await response.text(), True)
            else: 
                return ContentResponse(req.url, req.parent_url, req.content_type, req.save_path, "", False)
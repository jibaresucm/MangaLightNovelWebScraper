import mysql.connector
from Database.contentRequest import ContentRequest

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "hex_web_scraper"
)

dbcursor = mydb.cursor()

class ContentRequestDAO():

  def addContentRequestEntry(self, contentRequest: ContentRequest):
    dbcursor.execute(f"INSERT INTO content_requests (url, content_type, parent_url, status, save_path) VALUES ('{contentRequest.url}', '{contentRequest.content_type}', '{contentRequest.parent_url}', 'Unrequested', '{contentRequest.save_path}');")
    mydb.commit()

  def getContentRequests(self) -> list:
    dbcursor.callproc("getRequestsForFetching")
    stored_it = dbcursor.stored_results()
    data = next(stored_it)
    data = data.fetchall()
    if(data):
      mydb.commit()
    
    ret = []
    for elem in data:
      ret.append(self.convertToContentRequest(elem[0], elem[1], elem[2], elem[3], elem[4]))
    

    return ret


  def setAsComplete(self, content_url):
    dbcursor.execute(f"UPDATE content_requests SET status = 'Completed' WHERE url = '{content_url}'")
    mydb.commit()
    
  def setAsFailed(self, content_url):
    dbcursor.execute(f"UPDATE content_requests SET status = 'Failed' WHERE url = '{content_url}'")
    mydb.commit()
  
  def convertToContentRequest(self, url, parent_url, content_type, status, save_path)-> ContentRequest:
    return ContentRequest(url, parent_url, content_type, status, save_path)
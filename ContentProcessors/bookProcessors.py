from bs4 import BeautifulSoup
from processor import Processor
#Cases wto parse chapters: chapters.size = 0, no nextButton, all chapters in 1 page, all chapters after 1 load more click, api requests

#Use the urls to fetch the chapter (page prefix and suffix) when possible
#Next option is apiCalls

#Returns a list of the links to all the chapters of a book

class BookProcessor(Processor):

    def __init__(self):
        super().__init__()

    def getChaptersLinkFromHTMLS(htmls: list, parent_url: str, chapter_list_css: str):
        chapters = []
        for elem in htmls:
            chapterssoup = BeautifulSoup(elem, "html.parser")
            chapterssoup = chapterssoup.select_one(chapter_list_css)

            chaptersSoup = chapterssoup.find_all("a")
            for c in chaptersSoup:
                chapters.append(parent_url + c["href"])
        
        return chapters

"""def processChapterHTMLSToText(chapters, bookName, text_container):
    try:
        dir = "./Novels/" + bookName
        os.mkdir(dir)
    except:
        print("Error making dir "+ dir +" it might already be created")

    chapter_count = 1
    for chap_url in chapters:
        html = requestsGet(chap_url)
        chapter_text = processTextChapterHtml(html, text_container)
        dir = "../Content/Novels/" + bookName + "/Chapter " + str(chapter_count) + ".txt"
        with open(dir, "w", encoding="utf-8") as file:
            file.write(chapter_text)
        chapter_count += 1
        time.sleep(3) """



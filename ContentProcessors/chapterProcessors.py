from bs4 import BeautifulSoup
from ContentProcessors.processor import Processor
from ContentProcessors.processedData import ProcessedData
from Database.contentRequest import ContentRequest

class Chapter():
    def __init__(self, save_path, content):
        self.save_path = save_path
        self.content = content

class TextChapter(Chapter):
    def __init__(self, save_path, text):
        super().__init__(save_path, "TextChapter")
        self.text = text

class ImageChapter(Chapter):
    def __init__(self, save_path):
        super().__init__(save_path, "ImageChapter")


class ChapterProcessor(Processor):
    
    def __init__(self, info_container):
        super().__init__()
        self.info_container = info_container

class ImageChapterProcessor(ChapterProcessor):

    def process(self, content):
        pagesoup = BeautifulSoup(content.data, "html.parser")

        if not pagesoup: return

        chapter_image_list = pagesoup.select_one(self.info_container)

        if not chapter_image_list: return

        chapter_image_list = chapter_image_list.find_all("img")
        if not chapter_image_list: return

        content_requests = []
        idx = 0
        for elem in chapter_image_list:
            content_requests.append(ContentRequest(elem["src"], content.parent_url, "image","", content.save_path + "/image" +str(idx) + ".webp"))
            idx += 1

        return ProcessedData("save_n_fetch", content_requests, ImageChapter(content.save_path))

class TextChapterProcessor(ChapterProcessor):

    def process(self, content):
        pagesoup = BeautifulSoup(content.data, "html.parser")

        if not pagesoup: return

        chapter_reader = pagesoup.select_one(self.info_container)
        if not chapter_reader: return

        chapter_content = chapter_reader.find_all("p")
        if not chapter_content: return

        chapter_text = ""
        for elem in chapter_content:
            elemtext = elem.text
            if(elemtext != "" and elemtext != "\n"):
                chapter_text += '\n' + elemtext.replace("\n", "")

        return ProcessedData("save", None, TextChapter(content.save_path +".txt", chapter_text))
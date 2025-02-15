from bs4 import BeautifulSoup
from ContentFetchers.contentResponse import ContentResponse
from processor import Processor

class ChapterSaveConfiguration():
    def __init__(self, save_path, content):
        self.save_path = save_path
        self.content = content

class ChapterProcessor(Processor):
    
    def __init__(self, info_container):
        super().__init__()
        self.info_container = info_container


class ImageChapterProcessor(ChapterProcessor):

    def process(self, content):
        chaptersoup = BeautifulSoup(content.data, "html.parser")

        if not chaptersoup: return

        chapter_image_list = chaptersoup.select_one(self.info_container)

        if not chapter_image_list: return

        chapter_image_list = chapter_image_list.find_all("img")
        if not chapter_image_list: return
        return chapter_image_list["src"]

class TextChapterProcessor(ChapterProcessor):

    def process(self, content):
        chaptersoup = BeautifulSoup(content.data, "html.parser")

        if not chaptersoup: return

        chapter_reader = chaptersoup.select_one(self.info_container)
        if not chapter_reader: return

        chapter_content = chapter_reader.find_all("p")
        if not chapter_content: return

        chapter_text = ""
        for elem in chapter_content:
            elemtext = elem.text
            if(elemtext != "" and elemtext != "\n"):
                chapter_text += '\n' + elemtext.replace("\n", "")
        return chapter_text
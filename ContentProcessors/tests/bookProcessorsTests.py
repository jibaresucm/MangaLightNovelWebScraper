import unittest
from ContentProcessors.bookProcessors import StandardBookProcessor
from ContentFetchers.contentResponse import ContentResponse


class TestBookProcessors(unittest.TestCase):

    def test_standard_book_processor(self):
        p = StandardBookProcessor("#list-chapter","","","text", ".title","ul.info-meta.info")
        html = ""
        with open("./ContentProcessors/tests/standardBookProcessorTestData.txt", "r", encoding= "UTF-8") as fd:
            html = fd.read()
        content = ContentResponse("test", "test", "test", "./test", html, True)
        ret = p.process(content)
        self.assertEqual(len(ret.fetch_list), 320, "Does not return the expected chapters")
        self.assertEqual(ret.action, "save_n_fetch", "The action of the processed data return is incorrect")
        book = ret.save_data
        print(book.name + " " + book.synopsis)
        #Add for the name in slug mode this-is-the-name
        #And that it is 
class ContentResponse():
    def __init__(self, url, parent_url, content_type, save_path, data, successful):
        self.url = url
        self.parent_url = parent_url
        self.content_type = content_type
        self.save_path = save_path
        self.data = data
        self.successful = successful
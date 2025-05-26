class ContentRequest():
  def __init__(self, url, parent_url, content_type, status, save_path):
    self.url = url
    self.parent_url = parent_url
    self.content_type = content_type
    self.status = status
    self.save_path = save_path
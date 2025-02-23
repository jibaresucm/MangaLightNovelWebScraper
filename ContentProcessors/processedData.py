class ProcessedData():
    def __init__(self, action: str, fetch_list: list, save_data, save_path: str):
        self.action = action
        self.fetch_list = fetch_list
        self.save_data = save_data

#Problem: we need a universal way to send data to save and request

#Solution: A global ProcessedData class with action("save", "fetch", "save_n_fetch") 
#Save saves the object in save_data to save_path
#Fetch fetches(Adds in database queue) the list in fetch_list(Content request list)

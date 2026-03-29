class DataHandler:
    def __init__(self,data):
        self.data=data
        self.index=0
    def stream_next(self):
        if self.index<len(self.data):
            row = self.data.iloc[self.index]    
            self.index+=1
            return row
        return None
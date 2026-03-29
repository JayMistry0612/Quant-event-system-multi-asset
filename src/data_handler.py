class DataHandler:
    def __init__(self,data):
        self.data=data
        self.index=0
        self.length = min(len(df) for df in data.values())

    def stream_next(self):
        if self.index<self.length:
            batch={}
            
            for symbol,df in self.data.items():
                batch[symbol]=df.iloc[self.index]
            
            self.index+=1
            return batch
        return None
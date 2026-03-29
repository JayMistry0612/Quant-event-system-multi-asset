class Execution:
    def execute(self,signal,data):
        price=data['Open']
        return signal,price
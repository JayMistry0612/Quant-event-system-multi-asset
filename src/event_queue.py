from collections import deque

class EventQueue:
    def __init__(self):
        self.events = deque()
    
    def put(self,event):
        self.events.append(event)
    
    def get(self):
        return self.events.popleft() if self.events else None
    def is_empty(self):
        return len(self.events) == 0
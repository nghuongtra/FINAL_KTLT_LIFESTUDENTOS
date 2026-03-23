class Feedback:
    def __init__(self,username=None,time=None,content=None):
        self.username=username
        self.time=time
        self.content=content
    def __str__(self):
        return self.username
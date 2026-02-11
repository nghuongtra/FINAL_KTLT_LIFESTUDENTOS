class Task:
    def __init__(self,title,content,deadline,deadlinetime,isfinish):
        self.title=title
        self.content=content
        self.deadline=deadline
        self.deadlinetime=deadlinetime
        self.isfinish=isfinish
        pass
    def __str__(self):
        return self.title
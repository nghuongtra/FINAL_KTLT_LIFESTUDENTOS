class User:
    def __init__(self,Id=None, Name=None, UserName=None, Password=None,Bestfriend=None):
        self.Id=Id
        self.Name=Name
        self.UserName=UserName
        self.Password=Password
        self.Bestfriend=Bestfriend
    def __str__(self):
        infor=f"{self.Id}\t{self.Name}\t{self.UserName}\t{self.Password}\t{self.Bestfriend}"
        return infor
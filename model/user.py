class User:
    def __init__(self,Id=None, Name=None, UserName=None, Password=None):
        self.Id=Id
        self.Name=Name
        self.UserName=UserName
        self.Password=Password
    def __str__(self):
        infor=f"{self.Id}\t{self.Name}\t{self.UserName}\t{self.Password}"
        return infor
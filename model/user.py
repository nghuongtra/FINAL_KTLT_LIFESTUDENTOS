class User:
   def __init__(self,Id=None, Name=None, UserName=None, Password=None,PhoneNumber=None,Email=None,createdAt=None, lastLogin=None):
       self.Id=Id
       self.Name=Name
       self.UserName=UserName
       self.Password=Password
       self.PhoneNumber=PhoneNumber
       self.Email=Email
       self.createdAt=createdAt
       self.lastLogin=lastLogin
   def __str__(self):
       infor=(f"{self.Id}\t{self.Name}\t{self.UserName}\t{self.Password}\t{self.PhoneNumber}\t{self.Email}\t{self.createdAt}\t{self.lastLogin}")
       return infor


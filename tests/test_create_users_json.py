from model.user import User
from model.users import Users

u=Users()
u1=User("1","Mary","mary","1234","0356142189",None, None)
u2=User("2","Peter","peter","1234","0769412117",None, None)
u3=User("3","John","john","1234","0123456789",None, None)
u4=User("4","Cook","cook","1234","0987654321",None, None)
u5=User("5","Bright","bright","1234","0845362412",None, None)

u.add_items([u1,u2,u3,u4,u5])
print("Danh sach nhan vien cong ty")
u.print_items()
print("Xuất dữ liệu Employees vào Json file")
u.export_json("../datasets/users.json")




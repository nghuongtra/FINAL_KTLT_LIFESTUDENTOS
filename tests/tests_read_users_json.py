from model.users import Users

u=Users()
u.import_json("../datasets/users.json")
print("Danh sach User")
u.print_items()
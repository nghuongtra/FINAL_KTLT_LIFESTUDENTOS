from model.expense import Expense
from model.expenses import Expenses
manager = Expenses()
manager.add_item(Expense("Mua giáo trình", 150000, "Học tập", "Sách TMĐT"))
manager.add_item(Expense("Trà sữa", 45000, "Ăn uống", "Cùng nhóm"))
manager.export_json("../datasets/expenses.json")
print("Kiểm tra thư mục datasets xem đã có file expenses.json chưa nhé!")
from model.task import Task
from model.tasks import Tasks

task = Tasks()
t1 = Task("Đi chợ", "Mua thịt, cá, rau", "2025-12-20", "14:00:00", False)
t2 = Task("Lau bàn", "Lau bộ bàn ghế long phượng khủng long", "2025-12-25", "17:00:00", False)
t3 = Task("Họp team", "Review đồ cuối kỳ", "2025-12-19", "19:00:00", True)
t4 = Task("làm Logic học", "làm slide logic học", "2026-01-24", "14:00:00", False)
task.add_items([t1, t2, t3, t4])
print("Danh sách công việc hiện tại")
task.print_items()
print("Xuất task ra Json:")
task.export_json("../datasets/tasks.json")
from model.insight import Insight
from model.insights import Insights
ins=Insights()
ins.import_json("../datasets/insights.json")
ins1 = Insight(3.2, "50%", 500000, "An Toàn", "Đã học giỏi lại còn qua lí tài chính tốt", "Tự nấu ăn tại nhà để có thể tiết kiệm thêm tiền", "shopping", "2026-02-13")
ins2 = Insight(3.4, "60%", 200000, "Cảnh báo", "Học tốt nhưng tiêu tiền hơi quá tay nhe!", "Hãy luôn đặt câu hỏi 'Thực sự mình có cần món đồ đó không?' trước khi mua.", "xe cộ", "2026-03-16")
ins3 = Insight(3.5, "70%", 100000, "Cảnh báo", "Học tốt nhưng tiêu tiền hơi quá tay nhe!", "Dùng 1 tài khoản để tiêu – 1 tài khoản để tiết kiệm, đừng để chung.", "mục đích khác", "2026-04-06")
ins4 = Insight(4.0, "85%", 250000, "An toàn", "Quản lý chi tiêu khá ổn, tiếp tục duy trì phong độ này!", "Có thể bắt đầu đầu tư nhỏ hoặc gửi tiết kiệm định kỳ.", "shopping", "2026-04-07")
ins5 = Insight(2.8, "45%", 500000, "Báo động", "Chi tiêu đang vượt mức kiểm soát, cần xem lại các khoản không cần thiết.", "Ghi chép lại toàn bộ chi tiêu trong 7 ngày để biết tiền đang đi đâu.", "đồ ăn thức uống", "2026-04-08")
ins6 = Insight(3.2, "60%", 150000, "An toàn", "Tình hình tài chính tạm ổn nhưng vẫn có thể tối ưu thêm.", "Đặt giới hạn chi tiêu tuần để tránh vượt ngân sách.", "cải thiện thói quen", "2026-04-09")
ins.add_items([ins1, ins2, ins3, ins4, ins5, ins6])
print("Danh sách công việc hiện tại")
ins.print_items()
print("Xuất task ra Json:")
ins.export_json("../datasets/insights.json")



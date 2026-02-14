from model.insight import Insight
from model.insights import Insights
ins=Insights()
ins.import_json("../datasets/insights.json")
ins1=Insight(3.2, 50%, 500.000,"An Toàn","Đã học giỏi lại còn qua lí tài chính tốt","Tự nấu ăn tại nhà để có thể tiết kiệm thêm tiền","shopping", "2026-02-13")
ins2=Insight(3.4,50%, 200.000,"Cảnh báo","Học tốt nhưng tiêu tiền hơi quá tay nhe!" )



      "gpa": 3.2,
      "tien_do": "50%",
      "so_du": "500.000",
      "short_comment": "An toàn",
      "advice": "Đã học giỏi lại còn quản lí tài chính tốt",
      "tips": "Tip: Tự nấu ăn ở nhà...",
      "top_spending": "shopping",
      "ngay_thang": "2026-02-13"

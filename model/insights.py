import json
from model.insight import Insight
from model.mycollections import MyCollections


class Insights(MyCollections):
    # Hàm ĐỌC dữ liệu từ file JSON vào list
    def import_json(self, filename):
        self.filename = filename
        self.list.clear()  # Xóa list cũ trước khi đọc

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Duyệt qua từng phần tử trong cái key "insights"
                for item in data['insights']:
                    # Tạo object Insight thủ công tại đây
                    obj = Insight(
                        gpa=item['gpa'],
                        tien_do=item['tien_do'],
                        so_du=item['so_du'],
                        short_comment=item['short_comment'],
                        advice=item['advice'],
                        tips=item['tips'],
                        top_spending=item['top_spending'],
                        ngay_thang=item['ngay_thang']
                    )
                    self.list.append(obj)
        except FileNotFoundError:
            # Nếu chưa có file thì thôi, không làm gì cả
            pass

    # Hàm GHI dữ liệu từ list ra file JSON (Giống hệt ảnh comingevents.py)
    def export_json(self, filename):
        self.filename = filename

        # Tạo cấu trúc dictionary tổng
        data = {'insights': []}

        # Duyệt qua danh sách các object Insight đang có trong RAM
        for item in self.list:
            # Tự tay đóng gói từng cái vào dict con
            data['insights'].append({
                'gpa': item.gpa,
                'tien_do': item.tien_do,
                'so_du': item.so_du,
                'short_comment': item.short_comment,
                'advice': item.advice,
                'tips': item.tips,
                'top_spending': item.top_spending,
                'ngay_thang': item.ngay_thang
            })

        # Ghi xuống file
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
import json
from model.insight import Insight
from model.mycollections import MyCollections

class Insights(MyCollections):
    def import_json(self, filename):
        self.filename = filename
        self.list.clear()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data['insights']:
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
            pass
    def export_json(self, filename):
        self.filename = filename
        data = {'insights': []}
        for item in self.list:
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
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
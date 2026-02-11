import json

from model.comingevent import UpcomingEvent
from model.mycollections import MyCollections


class Upcomingevents(MyCollections):
    def export_json(self,filename):
        self.filename=filename
        data = {'upcomingevents': []}
        for item in self.list:
            data['upcomingevents'].append({
                'Date_Month': item.date_month,
                'Sukien': item.sukien,
        })

        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)  # xuống dòng/thụt dòng 4

    def import_json(self, filename):
        self.filename=filename
        self.list.clear()
        with open(filename, encoding='utf8') as json_file:
            data = json.load(json_file)
            for item in data['upcomingevents']:
                Date_Month= item['Date_Month']
                Sukien = item['Sukien']
                ucv=UpcomingEvent(Date_Month,Sukien)
                self.add_item(ucv)
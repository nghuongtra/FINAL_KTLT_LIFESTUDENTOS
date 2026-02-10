import json

from model.mycollections import MyCollections
from model.subject import Subject


class Subjects (MyCollections):
    def export_json(self, filename):
        self.filename=filename
        data = {"subjects": []}
        for i in self.list:
            data['subjects'].append({
                'Subid': i.Subid,
                'Subname': i.Subname,
                'credit': i.credit,
                'scoreProcess': i.scoreProcess,
                'scoreMidterm': i.scoreMidterm,
                'scoreFinal': i.scoreFinal
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    def import_json(self,filename):
        self.filename=filename
        self.list.clear()
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for i in data['subjects']:
                Subid=i["Subid"]
                Subname=i["Subname"]
                credit=i["credit"]
                scoreProcess=i["scoreProcess"]
                scoreMidterm=i["scoreMidterm"]
                scoreFinal=i["scoreFinal"]
            sub= Subject(Subid,Subname,credit,scoreProcess,scoreMidterm,scoreFinal)
            self.add_item(sub)

# from model.subject import Subject
# from model.mycollections import MyCollections
# import json
#
#
# class Subjects(MyCollections):
#   def __init__(self, filename="subjects.json"):
#       super().__init__()  # Khởi tạo lớp cha MyCollections
#       self.filename = filename
#
#   def export_json(self, filename=None):
#       if filename: self.filename = filename
#       data = {"subjects": []}
#       for i in self.list:
#           data['subjects'].append({
#               'Subname': i.Subname,
#               "credit": i.credit,
#               'scoreProcess': i.scoreProcess,
#               'scoreMidterm': i.scoreMidterm,
#               'scoreFinal': i.scoreFinal
#           })
#       with open(self.filename, 'w', encoding='utf-8') as outfile:
#           json.dump(data, outfile, ensure_ascii=False, indent=4)
#
#
#
#
#   def import_json(self, filename=None):
#       if filename: self.filename = filename
#       self.list.clear()
#       try:
#           with open(self.filename, encoding='utf-8') as json_file:
#               data = json.load(json_file)
#               for i in data['subjects']:
#                   sub = Subject(i["Subname"],
#                                 (i["credit"]),
#                       float(i["scoreProcess"]), float(i["scoreMidterm"]), float(i["scoreFinal"]))
#                   self.list.append(sub)
#       except FileNotFoundError:
#           print("File chưa tồn tại, sẽ tạo mới khi lưu.")
#
#
#
#
#   def find_item(self,Subname):
#       item = None
#       for it in self.list:
#           if it.Subname == Subname:
#               item = it
#               break
#       return item
#
#
#
#
#   def add_item(self, item):
#       exist_item = self.find_item(item.Subname)
#       if exist_item == None:
#           self.list.append(item)
#       else:
#           exist_item.Subname = item.Subname
#           exist_item.credit = item.credit
#           exist_item.scoreProcess = item.scoreProcess
#           exist_item.scoreMidterm = item.scoreMidterm
#           exist_item.scoreFinal = item.scoreFinal
#       self.export_json(self.filename)
#
#
#
#
#   def update_item(self, Subname, new_credit, new_process, new_mid, new_final):
#       item = self.find_item(Subname)
#       if item:
#           item.credit = new_credit
#           item.scoreProcess = new_process
#           item.scoreMidterm = new_mid
#           item.scoreFinal = new_final
#           self.export_json()
#           return True
#       return False
#
#
#
#
#   def delete_item(self, Subname):
#       item = self.find_item(Subname)
#       if item == None:
#           return False
#       self.list.remove(item)
#       self.export_json(self.filename)
#       return True
#
#
#
from model.subject import Subject
from model.mycollections import MyCollections
import json

class Subjects(MyCollections):
    def __init__(self, filename="subjects.json"):
        super().__init__()
        self.filename = filename

    def export_json(self, filename=None):
        if filename: self.filename = filename
        data = {"subjects": []}
        for i in self.list:
            data['subjects'].append({
                'Subname': i.Subname,
                'credit': i.credit,
                'components': i.components # Lưu toàn bộ mảng điểm động
            })
        with open(self.filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename=None):
        if filename: self.filename = filename
        self.list.clear()
        try:
            with open(self.filename, encoding='utf-8') as json_file:
                data = json.load(json_file)
                for i in data.get('subjects', []):
                    # Lấy dữ liệu an toàn bằng dict.get()
                    sub = Subject(
                        Subname=i["Subname"],
                        credit=int(i.get("credit", 0)),
                        components=i.get("components", [])
                    )
                    self.list.append(sub)
        except FileNotFoundError:
            print("File chưa tồn tại, sẽ tự động tạo khi có dữ liệu mới.")

    def find_item(self, Subname):
        for it in self.list:
            if it.Subname == Subname:
                return it
        return None

    def add_item(self, item):
        exist_item = self.find_item(item.Subname)
        if exist_item is None:
            self.list.append(item)
        else:
            # Nếu môn học đã tồn tại thì cập nhật
            exist_item.credit = item.credit
            exist_item.components = item.components
        self.export_json(self.filename)

    def delete_item(self, Subname):
        item = self.find_item(Subname)
        if item:
            self.list.remove(item)
            self.export_json(self.filename)
            return True
        return False
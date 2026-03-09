import json

from model.mycollections import MyCollections
from model.user import User


class Users(MyCollections):
    def export_json(self,filename):
        self.filename=filename
        data = {'users': []}
        for item in self.list:
            data['users'].append({
                'Id': item.Id,
                'Name': item.Name,
                'UserName': item.UserName,
                'Password': item.Password,
                'Phonenumber': item.Phonenumber,
                'createdAt': item.createdAt,
                'lastLogin': item.lastLogin,

        })

        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)  # xuống dòng/thụt dòng 4

    def import_json(self,filename):
        self.filename=filename
        self.list.clear()
        with open(filename, encoding='utf8') as json_file:
            data = json.load(json_file)
            for item in data['users']:
                Id=item['Id']
                Name=item['Name']
                UserName=item['UserName']
                Password=item['Password']
                Phonenumber=item['Phonenumber']
                createdAt=item['createdAt']
                lastLogin=item['lastLogin']
                emp=User(Id,Name,UserName,Password,Phonenumber,createdAt,lastLogin)
                self.add_item(emp)

    def login(self,uid,pwd):
        emp=None
        for item in self.list:
            if item.UserName == uid and item.Password == pwd:
                emp=item
                break
        return emp


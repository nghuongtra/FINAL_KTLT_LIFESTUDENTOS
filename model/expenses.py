import json
import os
from model.expense import Expense
class Expenses:
    def __init__(self):
        self.items=[]
    def add_item(self,item):
        self.items.append(item)
    def load_json(self,file_path):
        if os.path.exists(file_path):
            with open(file_path,'r',encoding='utf-8') as f:
                data =json.load(f)
                self.items=[Expense(**item) for item in data]
    def export_json(self,file_path):
        data=[item.to_dict() for item in self.items]
        with open(file_path,'w', encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

import json

from model.mycollections import MyCollections
from model.task import Task


class Tasks(MyCollections):
    def export_json(self, filename):
        self.filename=filename
        data = {"tasks": []}
        for i in self.list:
            data['tasks'].append({
                'title': i.title,
                'content': i.content,
                'deadline': str(i.deadline),
                'deadlinetime': str(i.deadlinetime),
                'isfinish': i.isfinish,
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    def import_json(self,filename):
        self.filename=filename
        self.list.clear()
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for i in data['tasks']:
                title=i["title"]
                content=i["content"]
                deadline=i["deadline"]
                deadlinetime=i["deadlinetime"]
                isfinish=i["isfinish"]
                task = Task(title=title, content=content, deadline=deadline,deadlinetime=deadlinetime, isfinish=isfinish)
                self.add_item(task)
    def item(self,index)->Task:
        return self.list[index]
    def index(self,task):
        i=self.list.index(task)
        return i
    def update(self,index,task)->Task:
        self.list[index]=task
        return self.list[index]
    def removeByIndex(self,index)->Task:
        return self.list.pop(index)
    def removeByItem(self,item):
        self.list.remove(item)
    def clear(self):
        self.list.clear()
    def size(self):
        return len(self.list)

import json
from model.mycollections import MyCollections
from model.feedback import Feedback


class Feedbacks(MyCollections):
    def export_json(self, filename):
        self.filename = filename
        data = {"feedbacks": []}
        for i in self.list:
            data['feedbacks'].append({
                'username': i.username,
                'time': i.time,
                'content': i.content,
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for i in data['feedbacks']:
                username = i["username"]
                time = i["time"]
                content = i["content"]
                feedback = Feedback(username=username, time=time, content=content)
                self.add_item(feedback)
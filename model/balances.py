import json
import os

class Balances:
    def __init__(self):
        self.current_balance = 0

    def load_json(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_balance = data.get("current_balance", 0)

    def export_json(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"current_balance": self.current_balance}, f, indent=4)
import json
import os
from datetime import datetime

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QTableWidgetItem, QListWidgetItem

from ui.AdminWindow import Ui_MainWindow
import resources_rc


class AdminWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlots()
        self.loadInitialData()

    def show(self):
        self.MainWindow.show()

    def setupSignalAndSlots(self):
        pass

    def loadInitialData(self):
        users_list = self.getUserData()
        self.labelTotalUser.setText(f"{len(users_list)} users")
        self.loadFeedbacks()
        self.listWidgetContact.setIconSize(QSize(30, 30))

        self.loadUsersToTable(users_list)
    def getUserData(self):
        with open('../datasets/users.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        users_list = data.get("users", [])
        return users_list

    def get_realtime_recent_activity(self, username):
        username_lower = username.lower()
        files_to_check = [
            f'../datasets/{username_lower}_tasks.json',
            f'../datasets/{username_lower}_expenses.json',
            f'../datasets/{username_lower}_balance.json'
        ]
        latest_time = 0
        activity_name = "Chưa có hoạt động"
        for filepath in files_to_check:
            if os.path.exists(filepath):
                mod_time = os.path.getmtime(filepath)
                if mod_time > latest_time:
                    latest_time = mod_time
                    if "tasks" in filepath:
                        activity_name = "Cập nhật Nhiệm vụ"
                    elif "expenses" in filepath:
                        activity_name = "Ghi chép Chi tiêu"
                    elif "balance" in filepath:
                        activity_name = "Cập nhật Số dư"
        if latest_time > 0:
            dt_object = datetime.fromtimestamp(latest_time)
            time_str = dt_object.strftime("%H:%M - %d/%m/%Y")
            return f"{activity_name} ({time_str})"
        return "Chưa có hoạt động"

    def loadUsersToTable(self, users_list):
        self.tableWidgetAdmin.setRowCount(0)
        for row_index, user in enumerate(users_list):
            self.tableWidgetAdmin.insertRow(row_index)
            user_id = str(user.get("Id", ""))
            username = str(user.get("UserName", ""))
            phone = str(
                user.get("PhoneNumber", ""))
            email = str(user.get("Email", ""))
            created_at = str(user.get("createdAt", "N/A"))
            last_login = str(user.get("lastLogin", "N/A"))
            realtime_activity = self.get_realtime_recent_activity(username)
            self.tableWidgetAdmin.setItem(row_index, 0, QTableWidgetItem(user_id))
            self.tableWidgetAdmin.setItem(row_index, 1, QTableWidgetItem(username))
            self.tableWidgetAdmin.setItem(row_index, 2, QTableWidgetItem(phone))
            self.tableWidgetAdmin.setItem(row_index, 3, QTableWidgetItem(email))
            self.tableWidgetAdmin.setItem(row_index, 4, QTableWidgetItem(created_at))
            self.tableWidgetAdmin.setItem(row_index, 5, QTableWidgetItem(last_login))
            self.tableWidgetAdmin.setItem(row_index, 6, QTableWidgetItem(realtime_activity))
    def loadFeedbacks(self):
        self.listWidgetContact.clear()
        feedback_file = "../datasets/feedbacks.json"
        with open(feedback_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        feedbacks = data.get("feedbacks", [])
        for fb in reversed(feedbacks):
            user = fb.get("username", "Unknown")
            time = fb.get("time", "")
            content = fb.get("content", "")
            display_text = f"Người dùng: {user}\nThời gian: {time}\nGóp ý: {content}\n{'-' * 55}"
            item = QListWidgetItem(display_text)
            item.setIcon(QIcon("../images/note.png"))
            item.setBackground(QColor("#F0F8FF"))
            self.listWidgetContact.addItem(item)




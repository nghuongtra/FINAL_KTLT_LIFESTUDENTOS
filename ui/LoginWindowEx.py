import datetime

from PyQt6.QtWidgets import QMessageBox, QMainWindow

import json
import os

from model.users import Users
from ui.ForgetPassWindowEx import ForgetPassWindowEx

from ui.LoginWindow import Ui_MainWindow
from ui.MainWindowEx import MainWindowEx
from ui.SigninWindowEx import SigninWindowEx


class LoginWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlots()
        self.lineEditUserName.setPlaceholderText("Username")
        self.lineEditPassword.setPlaceholderText("Password")
        self.process_save()

    def show(self):
        self.MainWindow.show()

    def setupSignalAndSlots(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.radioButtonSaveLogin.clicked.connect(self.process_save)
        self.pushButtonExit.clicked.connect(self.process_exit)
        self.pushButtonSignup.clicked.connect(self.process_signin)
        self.pushButtonfprget.clicked.connect(self.process_forget)
    def process_save(self):
        file_path = "../datasets/remember_me.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.lineEditUserName.setText(data.get("uid", ""))
                self.lineEditPassword.setText(data.get("pwd", ""))
                self.radioButtonSaveLogin.setChecked(True)
    def process_login(self, setText=None):
        uid=self.lineEditUserName.text()
        pwd=self.lineEditPassword.text()
        if uid == "admin" and pwd == "123457":
            from ui.AdminWindowEx import AdminWindowEx

            self.admin_window = QMainWindow()
            self.admin_ui = AdminWindowEx()
            self.admin_ui.setupUi(self.admin_window)

            self.MainWindow.close()
            self.admin_window.show()
            return
        le = Users()
        le.import_json("../datasets/users.json")
        usr=le.login(uid,pwd)
        if usr is None:
            self.msg = QMessageBox()
            self.msg.setText("Tên đăng nhập hoặc mật khẩu không chính xác!")
            self.msg.show()
        else:
            # CẬP NHẬT LAST LOGIN
            usr.lastLogin = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
            le.export_json("../datasets/users.json")
            # CHỈ LƯU KHI ĐĂNG NHẬP THÀNH CÔNG
            file_path = "../datasets/remember_me.json"
            if self.radioButtonSaveLogin.isChecked():
                dict_luu = {"uid": uid, "pwd": pwd}
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(dict_luu, f, ensure_ascii=False, indent=4)
            else:
                if os.path.exists(file_path):
                    os.remove(file_path)
            self.user_window = QMainWindow()
            self.as_ui = MainWindowEx()
            self.as_ui.login_employee = usr
            self.as_ui.current_acc = uid #ghi nhớ tên acc đăng nhập
            self.as_ui.setupUi(self.user_window)
            self.MainWindow.close()
            self.as_ui.show()
    def process_exit(self):
        self.MainWindow.close()
    def process_signin(self):
        # Tạo cửa sổ mới
        self.signin_window = QMainWindow()
        self.as_ui_signin = SigninWindowEx()  # Đổi tên biến để tránh nhầm lẫn
        self.as_ui_signin.setupUi(self.signin_window)
        # Đóng cái cũ, mở cái mới
        self.signin_window.show()
        self.MainWindow.close()

    def process_forget(self):
        from ui.ForgetPassWindowEx import ForgetPassWindowEx
        self.forget_window = QMainWindow()
        self.as_ui_forget = ForgetPassWindowEx()
        self.as_ui_forget.setupUi(self.forget_window)
        self.forget_window.show()
        self.MainWindow.close()

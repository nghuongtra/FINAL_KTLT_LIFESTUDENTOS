from PyQt6.QtWidgets import QMessageBox, QMainWindow

from ui.ForgetPassWindow import Ui_MainWindow


class ForgetPassWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlots()

    def show(self):
        self.MainWindow.show()

    def setupSignalAndSlots(self):
        self.pushButtonsubmit.clicked.connect(self.process_password)

    def process_password(self):
        phonenumber = self.lineEditfriend.text().strip()

        if phonenumber == "":
            msg = QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Vui lòng nhập thông tin để lấy mật khẩu!")
            msg.exec()
            return

        from model.users import Users
        all_users = Users()

        try:
            all_users.import_json("../datasets/users.json")
        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            return

        # 1. Tạo một danh sách để chứa tất cả các user khớp điều kiện
            # 1. Tạo một danh sách để chứa tất cả các user khớp điều kiện
        found_users_list = []
        for user in all_users.list:
            if str(user.Phonenumber).strip() == phonenumber:
                found_users_list.append(user)

        # 2. Kiểm tra xem danh sách có dữ liệu không
        if len(found_users_list) > 0:
            # 3. Duyệt danh sách để nối chuỗi thông tin của tất cả tài khoản
            message_text = f"Tìm thấy {len(found_users_list)} tài khoản có cùng số điện thoại:\n\n"

            for i, user in enumerate(found_users_list, 1):
                message_text += f"Tài khoản {i}:\n"
                message_text += f" ➤ Username: {user.UserName}\n"
                message_text += f" ➤ Password: {user.Password}\n"
                message_text += "-" * 20 + "\n"

            msg = QMessageBox()
            msg.setWindowTitle("Thông tin tài khoản")
            msg.setText(message_text)
            msg.exec()

            self.go_back_to_login()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText("Không tìm thấy tài khoản nào trùng với số điện thoại này!")
            msg.exec()

    def go_back_to_login(self):
        from ui.LoginWindowEx import LoginWindowEx

        self.login_window = QMainWindow()
        self.login_ui = LoginWindowEx()
        self.login_ui.setupUi(self.login_window)

        self.MainWindow.close()  # Đóng cửa sổ quên mật khẩu hiện tại
        self.login_window.show()  # Mở cửa sổ đăng nhập
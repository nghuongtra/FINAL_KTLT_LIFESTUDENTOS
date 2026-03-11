from PyQt6.QtWidgets import QMessageBox, QMainWindow
from ui.ForgetPassWindow import Ui_MainWindow
from model.auth_handler import AuthManager


class ForgetPassWindowEx(Ui_MainWindow):
   def setupUi(self, MainWindow):
       super().setupUi(MainWindow)
       self.MainWindow = MainWindow
       self.auth = AuthManager()  # Khởi tạo bộ máy gửi mail
       self.setupSignalAndSlots()


   def show(self):
       self.MainWindow.show()


   def setupSignalAndSlots(self):
       self.pushButtonsubmit.clicked.connect(self.process_password)


   def process_password(self):
       phone_input = self.lineEditfriend.text().strip()


       if phone_input == "":
           QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng nhập số điện thoại!")
           return


       from model.users import Users
       all_users = Users()
       all_users.import_json("../datasets/users.json")


       # 1. Tìm user khớp SĐT
       found_user = next((u for u in all_users.list if str(u.PhoneNumber).strip() == phone_input), None)


       if found_user:
           #Kiểm tra xem user có email không
           if not found_user.Email:
               QMessageBox.critical(self.MainWindow, "Lỗi", "Tài khoản này chưa đăng ký Email!")
               return


           success = self.auth.send_password_to_mail(
               found_user.Email,
               found_user.Name,
               found_user.Password
           )


           if success:
               QMessageBox.information(self.MainWindow, "Thành công",
                                       f"Mật khẩu đã được gửi đến email: {found_user.Email}")
               self.go_back_to_login()
           else:
               QMessageBox.critical(self.MainWindow, "Lỗi", "Không thể gửi email!")
       else:
           QMessageBox.warning(self.MainWindow, "Lỗi", "Số điện thoại không tồn tại trong hệ thống!")


   def go_back_to_login(self):
       from ui.LoginWindowEx import LoginWindowEx
       self.login_window = QMainWindow()
       self.login_ui = LoginWindowEx()
       self.login_ui.setupUi(self.login_window)
       self.MainWindow.close()
       self.login_window.show()


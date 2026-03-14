import datetime


from PyQt6.QtWidgets import QMessageBox, QMainWindow


from model.user import User
from model.users import Users


from ui.SigninWindow import Ui_MainWindow




class SigninWindowEx(Ui_MainWindow):
   def setupUi(self, MainWindow):
       super().setupUi(MainWindow)
       self.MainWindow = MainWindow
       self.setupSignalAndSlots()


   def setupSignalAndSlots(self):
       self.pushButtonsave.clicked.connect(self.process_save)
       self.pushButtonexit.clicked.connect(self.process_back)


   def process_back(self):
       from ui.LoginWindowEx import LoginWindowEx


       self.login_window = QMainWindow()
       self.login_ui = LoginWindowEx()
       self.login_ui.setupUi(self.login_window)


       self.MainWindow.close()
       self.login_window.show()


   def process_save(self):
       name = self.lineEditname.text()
       uid = self.lineEditusername.text()
       pwd = self.lineEditpass.text()
       phone = self.lineEditPhoneNumber.text()
       email = self.lineEditusername_8.text().strip()


       if name == "" or uid == "" or pwd == "":
           msg = QMessageBox()
           msg.setText("Yêu cầu nhập đầy đủ thông tin!")
           msg.exec()
           return


       # 1. Đọc danh sách hiện có
       all_users = Users()
       # Chú ý đường dẫn file tương ứng với cấu trúc folder của bạn
       all_users.import_json("../datasets/users.json")


       # 2. Tạo ID mới (bằng cách lấy số lượng hiện tại + 1)
       new_id = len(all_users.list) + 1
       created_at = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
       new_user = User(new_id, name, uid, pwd, phone, email,created_at, None)


       # 3. Thêm vào danh sách và xuất ra file JSON
       all_users.add_item(new_user)
       all_users.export_json("../datasets/users.json")


       # 4. Thông báo và quay lại trang đăng nhập
       # 3. HIỆN THÔNG BÁO VÀ TỰ QUAY VỀ TRANG LOGIN
       msg = QMessageBox()
       msg.setText("Đăng ký thành công! Đang quay lại trang đăng nhập...")
       msg.exec()  # Đợi người dùng bấm OK


       from ui.LoginWindowEx import LoginWindowEx
       self.login_window = QMainWindow()
       self.login_ui = LoginWindowEx()
       self.login_ui.setupUi(self.login_window)


       self.MainWindow.close()
       self.login_window.show()


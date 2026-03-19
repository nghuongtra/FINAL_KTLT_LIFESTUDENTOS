import json
import os

from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from model.subject import Subject
from model.subjects import Subjects

class AcademicController:
   def __init__(self, main_view):
       self.view = main_view
       self.sub_manager = Subjects()
   def setup(self):
       self.file_subject = f"../datasets/{self.current_acc}_subjects.json"
       if not os.path.exists(self.file_subject):
           with open(self.file_subject, "w", encoding="utf-8") as f: f.write('{"subjects": []}')
       self.sub_manager = Subjects()
       self.sub_manager.import_json(self.file_subject)
       self.display_subjects()
       self.view.lineEditGPA.setReadOnly(True)
       self.view.lineEditXeploai.setReadOnly(True)
       self.view.lineEditTimmon.setText("")
       self.view.lineEditTimmon.setPlaceholderText("Tìm kiếm môn học...")

   def clear_inputs(self):
       self.view.NameLineEdit.clear()
       self.view.CreditLineEdit.clear()
       self.view.ProcessLineEdit.clear()
       self.view.MidtermLineEdit.clear()
       self.view.FinalLineEdit.clear()
       self.view.lineEditGPA.clear()
       self.view.lineEditXeploai.clear()

   def display_subjects(self,data_list=None):
       items = data_list if data_list is not None else self.sub_manager.list
       self.view.tableWidgetthongtinmon.setRowCount(0)
       for item in items:
           row_index = self.view.tableWidgetthongtinmon.rowCount()
           self.view.tableWidgetthongtinmon.insertRow(row_index)
           self.view.tableWidgetthongtinmon.setItem(row_index, 0, QTableWidgetItem(str(item.Subname)))
           self.view.tableWidgetthongtinmon.setItem(row_index, 1, QTableWidgetItem(str(item.credit)))
           self.view.tableWidgetthongtinmon.setItem(row_index, 2, QTableWidgetItem(str(item.scoreProcess)))
           self.view.tableWidgetthongtinmon.setItem(row_index, 3, QTableWidgetItem(str(item.scoreMidterm)))
           self.view.tableWidgetthongtinmon.setItem(row_index, 4, QTableWidgetItem(str(item.scoreFinal)))

   def process_calculate_gpa(self):
       # Kiểm tra xem các dữ liệu bắt buộc có bị bỏ trống hay không
       input_fields = [
           self.view.ProcessLineEdit.text(),
           self.view.MidtermLineEdit.text(),
           self.view.FinalLineEdit.text()
       ]
       if any(field.strip() == "" for field in input_fields):
           QMessageBox.warning(self.view.MainWindow, "Thông báo", "Vui lòng nhập đầy đủ các đầu điểm!")
           return
       try:
           sub_name = self.view.NameLineEdit.text().strip()
           credit = int(self.view.CreditLineEdit.text() or 0)
           process = float(self.view.ProcessLineEdit.text())
           midterm = float(self.view.MidtermLineEdit.text())
           final = float(self.view.FinalLineEdit.text())
           # Kiểm tra  giá trị điểm
           if not (0 <= process <= 10 and 0 <= midterm <= 10 and 0 <= final <= 10):
               QMessageBox.warning(self.view.MainWindow, "Lỗi dữ liệu", "Điểm số phải nằm trong khoảng từ 0 đến 10!")
               return
           temp_sub = Subject(sub_name, credit, process, midterm, final)
           gpa_score = temp_sub.tinh_diem_gpa()
           self.view.lineEditGPA.setText(f"{gpa_score:.2f}")
           classification = temp_sub.tinh_xep_loai()
           self.view.lineEditXeploai.setText(classification)
       except ValueError:
           QMessageBox.warning(self.view.MainWindow, "Lỗi định dạng",
                               "Số tín chỉ và điểm số phải là định dạng số hợp lệ!")

   def process_add_subject(self):
       try:
           tong_tin_chi = 0
           tong_diem = 0.0
           for mon in self.view.sub_manager.list:
               tin_chi = float(mon.credit)
               diem_so = (float(mon.scoreProcess) * 0.2) + (float(mon.scoreMidterm) * 0.3) + (
                           float(mon.scoreFinal) * 0.5)
               tong_tin_chi += tin_chi
               tong_diem += (diem_so * tin_chi)
           gpa_cu = 0.0
           if tong_tin_chi > 0:
               gpa_cu = tong_diem / tong_tin_chi
           path = f"../datasets/{self.current_acc}_gpa_user.json"
           with open(path, "w", encoding="utf-8") as f:
               json.dump({"gpa_ky_truoc": gpa_cu}, f, indent=4)
       except Exception as e:
           pass

       Subname = self.view.NameLineEdit.text()
       credit = self.view.CreditLineEdit.text()
       process = self.view.ProcessLineEdit.text()
       midterm = self.view.MidtermLineEdit.text()
       final = self.view.FinalLineEdit.text()
       if Subname == "":
           QMessageBox.warning(self.view.MainWindow, "Lỗi", "Tên môn không được để trống!")
           return
       # Kiểm tra môn này đã có chưa
       if self.sub_manager.find_item(Subname) is not None:
           QMessageBox.warning(self.view.MainWindow, "Lỗi",
                               f"Môn '{Subname}' đã tồn tại! Vui lòng dùng nút Edit")
           self.clear_inputs()
           self.view.NameLineEdit.setFocus()
           return
       # Lưu file và cập nhật bảng
       item = Subject(Subname, credit, process, midterm, final)
       self.sub_manager.add_item(item)
       self.sub_manager.export_json(self.file_subject)
       self.display_subjects()
       self.clear_inputs()
       QMessageBox.information(self.view.MainWindow, "Thông báo", "Đã thêm môn học mới thành công!")

   def process_selection(self):
       selected_row = self.view.tableWidgetthongtinmon.currentRow()
       if selected_row < 0:
           return
       try:
           Subname = self.view.tableWidgetthongtinmon.item(selected_row, 0).text()
           credit = self.view.tableWidgetthongtinmon.item(selected_row, 1).text()
           scoreProcess = self.view.tableWidgetthongtinmon.item(selected_row, 2).text()
           scoreMidterm = self.view.tableWidgetthongtinmon.item(selected_row, 3).text()
           scoreFinal = self.view.tableWidgetthongtinmon.item(selected_row, 4).text()

           self.view.NameLineEdit.setText(Subname)
           self.view.CreditLineEdit.setText(str(credit))
           self.view.ProcessLineEdit.setText(str(scoreProcess))
           self.view.MidtermLineEdit.setText(str(scoreMidterm))
           self.view.FinalLineEdit.setText(str(scoreFinal))
           self.view.lineEditGPA.setText("")
           self.view.lineEditXeploai.setText("")
       except AttributeError:  # Phòng trường hợp ô trống
           pass

   def process_edit_subject(self):
       try:
           tong_tin_chi = 0
           tong_diem = 0.0
           for mon in self.view.sub_manager.list:
               tin_chi = float(mon.credit)
               diem_so = (float(mon.scoreProcess) * 0.2) + (float(mon.scoreMidterm) * 0.3) + (
                           float(mon.scoreFinal) * 0.5)
               tong_tin_chi += tin_chi
               tong_diem += (diem_so * tin_chi)
           gpa_cu = 0.0
           if tong_tin_chi > 0:
               gpa_cu = tong_diem / tong_tin_chi
           path = f"../datasets/{self.current_acc}_gpa_user.json"
           with open(path, "w", encoding="utf-8") as f:
               json.dump({"gpa_ky_truoc": gpa_cu}, f, indent=4)
       except Exception as e:
           pass

       Subname = self.view.NameLineEdit.text()
       if Subname == "":
           QMessageBox.warning(self.view.MainWindow, "Lỗi", "Vui lòng chọn môn cần sửa!")
           return
       # Tìm môn học trong danh sách dựa theo tên
       existing_sub = self.sub_manager.find_item(Subname)
       if existing_sub is None:
           QMessageBox.warning(self.view.MainWindow, "Lỗi",
                               f"Không tìm thấy môn '{Subname}' để sửa! Vui lòng dùng nút Add (Thêm).")
           return

       # Cập nhật thông tin mới vào đối tượng tìm thấy
       try:
           existing_sub.credit = int(self.view.CreditLineEdit.text() or 0)
           existing_sub.scoreProcess = float(self.view.ProcessLineEdit.text() or 0)
           existing_sub.scoreMidterm = float(self.view.MidtermLineEdit.text() or 0)
           existing_sub.scoreFinal = float(self.view.FinalLineEdit.text() or 0)
       except ValueError:
           QMessageBox.warning(self.view.MainWindow, "Lỗi", "Số liệu nhập vào không hợp lệ!")
           return
       self.sub_manager.export_json(self.file_subject)
       self.display_subjects()
       QMessageBox.information(self.view.MainWindow, "Thông báo", f"Đã cập nhật thông tin môn {Subname}!")

   def process_delete_subject(self):
       try:
           tong_tin_chi = 0
           tong_diem = 0.0
           for mon in self.view.sub_manager.list:
               tin_chi = float(mon.credit)
               diem_so = (float(mon.scoreProcess) * 0.2) + (float(mon.scoreMidterm) * 0.3) + (
                           float(mon.scoreFinal) * 0.5)
               tong_tin_chi += tin_chi
               tong_diem += (diem_so * tin_chi)
           gpa_cu = 0.0
           if tong_tin_chi > 0:
               gpa_cu = tong_diem / tong_tin_chi
           path = f"../datasets/{self.current_acc}_gpa_user.json"
           with open(path, "w", encoding="utf-8") as f:
               json.dump({"gpa_ky_truoc": gpa_cu}, f, indent=4)
       except Exception as e:
           pass

       Subname = self.view.NameLineEdit.text()
       if Subname == "":
           QMessageBox.critical(self.view.MainWindow, "Lỗi xóa", "Bạn phải chọn một môn học để xóa!")
           return
       dlg = QMessageBox.question(
           self.view.MainWindow,
           "Xác nhận xóa",
           f"Bạn có chắc chắn muốn xóa môn [{Subname}] không?",
           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
       if dlg == QMessageBox.StandardButton.Yes:
           ret = self.sub_manager.delete_item(Subname)
           if ret:
               self.sub_manager.export_json(self.file_subject)
               self.display_subjects()
               self.clear_inputs()
               QMessageBox.information(self.view.MainWindow, "Thông báo", "Đã xóa thành công!")
           else:
               QMessageBox.warning(self.view.MainWindow, "Lỗi", "Không tìm thấy môn học trong dữ liệu!")

   def search_subject(self):
       keyword = self.view.lineEditTimmon.text().strip().lower()
       # Lọc danh sách môn học khớp với từ khóa
       filtered_list = [item for item in self.sub_manager.list if keyword in item.Subname.lower()]
       self.display_subjects(filtered_list)
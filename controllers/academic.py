from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from model.subject import Subject
from model.subjects import Subjects


class AcademicController:
    def __init__(self, main_view):
        self.view = main_view
        self.sub_manager = Subjects()
    def setup(self):
        self.sub_manager = Subjects()
        self.sub_manager.import_json("../datasets/subjects.json")
        self.display_subjects()
        self.view.lineEditTimmon.setText("")
        self.view.lineEditTimmon.setPlaceholderText("Tìm kiếm môn học...")
    def process_calculate_gpa(self):
        if self.view.NameLineEdit.text() == "" or self.view.ProcessLineEdit.text() == "":
            QMessageBox.warning(self.view.MainWindow, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return
        ten = self.view.NameLineEdit.text()
        tin_chi = int(self.view.CreditLineEdit.text() or 0)
        qt = float(self.view.ProcessLineEdit.text() or 0)
        gk = float(self.view.MidtermLineEdit.text() or 0)
        ck = float(self.view.FinalLineEdit.text() or 0)
        # Tạo đối tượng tạm thời để tính toán
        temp_sub = Subject(ten, tin_chi, qt, gk, ck)
        # Hiển thị kết quả lên giao diện
        self.view.lineEditGPA.setText(str(temp_sub.tinh_diem_gpa()))
        self.view.lineEditXeploai.setText(temp_sub.tinh_xep_loai())


    def process_add_subject(self):
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
            self.view.NameLineEdit.setText("")
            self.view.CreditLineEdit.setText("")
            self.view.ProcessLineEdit.setText("")
            self.view.MidtermLineEdit.setText("")
            self.view.FinalLineEdit.setText("")
            self.view.NameLineEdit.setFocus()
            return
        # Lưu file và cập nhật bảng
        item = Subject(Subname, credit, process, midterm, final)
        self.sub_manager.add_item(item)
        self.sub_manager.export_json()
        self.display_subjects()
        self.view.NameLineEdit.clear()
        self.view.CreditLineEdit.clear()
        self.view.ProcessLineEdit.clear()
        self.view.MidtermLineEdit.clear()
        self.view.FinalLineEdit.clear()
        QMessageBox.information(self.view.MainWindow, "Thông báo", "Đã thêm môn học mới thành công!")


    def display_subjects(self):
        self.view.tableWidgetthongtinmon.setRowCount(0)
        for item in self.sub_manager.list:
            row_index = self.view.tableWidgetthongtinmon.rowCount()
            self.view.tableWidgetthongtinmon.insertRow(row_index)
            self.view.tableWidgetthongtinmon.setItem(row_index, 0, QTableWidgetItem(str(item.Subname)))
            self.view.tableWidgetthongtinmon.setItem(row_index, 1, QTableWidgetItem(str(item.credit)))
            self.view.tableWidgetthongtinmon.setItem(row_index, 2, QTableWidgetItem(str(item.scoreProcess)))
            self.view.tableWidgetthongtinmon.setItem(row_index, 3, QTableWidgetItem(str(item.scoreMidterm)))
            self.view.tableWidgetthongtinmon.setItem(row_index, 4, QTableWidgetItem(str(item.scoreFinal)))


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
        # Lưu file và cập nhật bảng
        self.sub_manager.export_json()
        self.display_subjects()
        QMessageBox.information(self.view.MainWindow, "Thông báo", f"Đã cập nhật thông tin môn {Subname}!")


    def process_delete_subject(self):
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
                self.sub_manager.export_json()
                self.display_subjects()
                QMessageBox.information(self.view.MainWindow, "Thông báo", "Đã xóa thành công!")
            else:
                QMessageBox.warning(self.view.MainWindow, "Lỗi", "Không tìm thấy môn học trong dữ liệu!")


    def search_subject(self):
        # Lấy từ khóa từ ô nhập liệu và chuyển về chữ thường để tìm chính xác hơn
        keyword = self.view.lineEditTimmon.text().strip().lower()
        # Xóa sạch bảng hiện tại
        self.view.tableWidgetthongtinmon.setRowCount(0)
        # Lọc và hiển thị; Duyệt qua danh sách môn học
        for item in self.sub_manager.list:
            if keyword in item.Subname.lower():
                row_index = self.view.tableWidgetthongtinmon.rowCount()
                self.view.tableWidgetthongtinmon.insertRow(row_index)
                self.view.tableWidgetthongtinmon.setItem(row_index, 0, QTableWidgetItem(str(item.Subname)))
                self.view.tableWidgetthongtinmon.setItem(row_index, 1, QTableWidgetItem(str(item.credit)))
                self.view.tableWidgetthongtinmon.setItem(row_index, 2, QTableWidgetItem(str(item.scoreProcess)))
                self.view.tableWidgetthongtinmon.setItem(row_index, 3, QTableWidgetItem(str(item.scoreMidterm)))
                self.view.tableWidgetthongtinmon.setItem(row_index, 4, QTableWidgetItem(str(item.scoreFinal)))
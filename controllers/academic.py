# import json
# import os
#
#
# from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
#
#
# from model.subject import Subject
# from model.subjects import Subjects
#
#
# class AcademicController:
#   def __init__(self, main_view):
#       self.view = main_view
#       self.sub_manager = Subjects()
#   def setup(self):
#       self.file_subject = f"../datasets/{self.current_acc}_subjects.json"
#       if not os.path.exists(self.file_subject):
#           with open(self.file_subject, "w", encoding="utf-8") as f: f.write('{"subjects": []}')
#       self.sub_manager = Subjects()
#       self.sub_manager.import_json(self.file_subject)
#       self.display_subjects()
#       self.view.lineEditGPA.setReadOnly(True)
#       self.view.lineEditXeploai.setReadOnly(True)
#       self.view.lineEditTimmon.setText("")
#       self.view.lineEditTimmon.setPlaceholderText("Tìm kiếm môn học...")
#
#
#   def clear_inputs(self):
#       self.view.NameLineEdit.clear()
#       self.view.CreditLineEdit.clear()
#       self.view.ProcessLineEdit.clear()
#       self.view.MidtermLineEdit.clear()
#       self.view.FinalLineEdit.clear()
#       self.view.lineEditGPA.clear()
#       self.view.lineEditXeploai.clear()
#
#
#   def display_subjects(self,data_list=None):
#       items = data_list if data_list is not None else self.sub_manager.list
#       self.view.tableWidgetthongtinmon.setRowCount(0)
#       for item in items:
#           row_index = self.view.tableWidgetthongtinmon.rowCount()
#           self.view.tableWidgetthongtinmon.insertRow(row_index)
#           self.view.tableWidgetthongtinmon.setItem(row_index, 0, QTableWidgetItem(str(item.Subname)))
#           self.view.tableWidgetthongtinmon.setItem(row_index, 1, QTableWidgetItem(str(item.credit)))
#           self.view.tableWidgetthongtinmon.setItem(row_index, 2, QTableWidgetItem(str(item.scoreProcess)))
#           self.view.tableWidgetthongtinmon.setItem(row_index, 3, QTableWidgetItem(str(item.scoreMidterm)))
#           self.view.tableWidgetthongtinmon.setItem(row_index, 4, QTableWidgetItem(str(item.scoreFinal)))
#
#
#   def process_calculate_gpa(self):
#       # Kiểm tra xem các dữ liệu bắt buộc có bị bỏ trống hay không
#       input_fields = [
#           self.view.ProcessLineEdit.text(),
#           self.view.MidtermLineEdit.text(),
#           self.view.FinalLineEdit.text()
#       ]
#       if any(field.strip() == "" for field in input_fields):
#           QMessageBox.warning(self.view.MainWindow, "Thông báo", "Vui lòng nhập đầy đủ các đầu điểm!")
#           return
#       try:
#           sub_name = self.view.NameLineEdit.text().strip()
#           credit = int(self.view.CreditLineEdit.text() or 0)
#           process = float(self.view.ProcessLineEdit.text())
#           midterm = float(self.view.MidtermLineEdit.text())
#           final = float(self.view.FinalLineEdit.text())
#           # Kiểm tra  giá trị điểm
#           if not (0 <= process <= 10 and 0 <= midterm <= 10 and 0 <= final <= 10):
#               QMessageBox.warning(self.view.MainWindow, "Lỗi dữ liệu", "Điểm số phải nằm trong khoảng từ 0 đến 10!")
#               return
#           temp_sub = Subject(sub_name, credit, process, midterm, final)
#           gpa_score = temp_sub.tinh_diem_gpa()
#           self.view.lineEditGPA.setText(f"{gpa_score:.2f}")
#           classification = temp_sub.tinh_xep_loai()
#           self.view.lineEditXeploai.setText(classification)
#       except ValueError:
#           QMessageBox.warning(self.view.MainWindow, "Lỗi định dạng",
#                               "Số tín chỉ và điểm số phải là định dạng số hợp lệ!")
#
#
#   def process_add_subject(self):
#       try:
#           tong_tin_chi = 0
#           tong_diem = 0.0
#           for mon in self.view.sub_manager.list:
#               tin_chi = float(mon.credit)
#               diem_so = (float(mon.scoreProcess) * 0.3) + (float(mon.scoreMidterm) * 0.2) + (
#                           float(mon.scoreFinal) * 0.5)
#               tong_tin_chi += tin_chi
#               tong_diem += (diem_so * tin_chi)
#           gpa_cu = 0.0
#           if tong_tin_chi > 0:
#               gpa_cu = tong_diem / tong_tin_chi
#           path = f"../datasets/{self.current_acc}_gpa_user.json"
#           with open(path, "w", encoding="utf-8") as f:
#               json.dump({"gpa_ky_truoc": gpa_cu}, f, indent=4)
#       except Exception as e:
#           pass
#
#
#       Subname = self.view.NameLineEdit.text()
#       credit = self.view.CreditLineEdit.text()
#       process = self.view.ProcessLineEdit.text()
#       midterm = self.view.MidtermLineEdit.text()
#       final = self.view.FinalLineEdit.text()
#       if Subname == "":
#           QMessageBox.warning(self.view.MainWindow, "Lỗi", "Tên môn không được để trống!")
#           return
#       # Kiểm tra môn này đã có chưa
#       if self.sub_manager.find_item(Subname) is not None:
#           QMessageBox.warning(self.view.MainWindow, "Lỗi",
#                               f"Môn '{Subname}' đã tồn tại! Vui lòng dùng nút Edit")
#           self.clear_inputs()
#           self.view.NameLineEdit.setFocus()
#           return
#       # Lưu file và cập nhật bảng
#       item = Subject(Subname, credit, process, midterm, final)
#       self.sub_manager.add_item(item)
#       self.sub_manager.export_json(self.file_subject)
#       self.display_subjects()
#       self.clear_inputs()
#       QMessageBox.information(self.view.MainWindow, "Thông báo", "Đã thêm môn học mới thành công!")
#
#
#   def process_selection(self):
#       selected_row = self.view.tableWidgetthongtinmon.currentRow()
#       if selected_row < 0:
#           return
#       try:
#           Subname = self.view.tableWidgetthongtinmon.item(selected_row, 0).text()
#           credit = self.view.tableWidgetthongtinmon.item(selected_row, 1).text()
#           scoreProcess = self.view.tableWidgetthongtinmon.item(selected_row, 2).text()
#           scoreMidterm = self.view.tableWidgetthongtinmon.item(selected_row, 3).text()
#           scoreFinal = self.view.tableWidgetthongtinmon.item(selected_row, 4).text()
#
#
#           self.view.NameLineEdit.setText(Subname)
#           self.view.CreditLineEdit.setText(str(credit))
#           self.view.ProcessLineEdit.setText(str(scoreProcess))
#           self.view.MidtermLineEdit.setText(str(scoreMidterm))
#           self.view.FinalLineEdit.setText(str(scoreFinal))
#           self.view.lineEditGPA.setText("")
#           self.view.lineEditXeploai.setText("")
#       except AttributeError:  # Phòng trường hợp ô trống
#           pass
#
#
#   def process_edit_subject(self):
#       try:
#           tong_tin_chi = 0
#           tong_diem = 0.0
#           for mon in self.view.sub_manager.list:
#               tin_chi = float(mon.credit)
#               diem_so = (float(mon.scoreProcess) * 0.3) + (float(mon.scoreMidterm) * 0.2) + (
#                           float(mon.scoreFinal) * 0.5)
#               tong_tin_chi += tin_chi
#               tong_diem += (diem_so * tin_chi)
#           gpa_cu = 0.0
#           if tong_tin_chi > 0:
#               gpa_cu = tong_diem / tong_tin_chi
#           path = f"../datasets/{self.current_acc}_gpa_user.json"
#           with open(path, "w", encoding="utf-8") as f:
#               json.dump({"gpa_ky_truoc": gpa_cu}, f, indent=4)
#       except Exception as e:
#           pass
#
#
#       Subname = self.view.NameLineEdit.text()
#       if Subname == "":
#           QMessageBox.warning(self.view.MainWindow, "Lỗi", "Vui lòng chọn môn cần sửa!")
#           return
#       # Tìm môn học trong danh sách dựa theo tên
#       existing_sub = self.sub_manager.find_item(Subname)
#       if existing_sub is None:
#           QMessageBox.warning(self.view.MainWindow, "Lỗi",
#                               f"Không tìm thấy môn '{Subname}' để sửa! Vui lòng dùng nút Add (Thêm).")
#           return
#
#
#       # Cập nhật thông tin mới vào đối tượng tìm thấy
#       try:
#           existing_sub.credit = int(self.view.CreditLineEdit.text() or 0)
#           existing_sub.scoreProcess = float(self.view.ProcessLineEdit.text() or 0)
#           existing_sub.scoreMidterm = float(self.view.MidtermLineEdit.text() or 0)
#           existing_sub.scoreFinal = float(self.view.FinalLineEdit.text() or 0)
#       except ValueError:
#           QMessageBox.warning(self.view.MainWindow, "Lỗi", "Số liệu nhập vào không hợp lệ!")
#           return
#       self.sub_manager.export_json(self.file_subject)
#       self.display_subjects()
#       QMessageBox.information(self.view.MainWindow, "Thông báo", f"Đã cập nhật thông tin môn {Subname}!")
#
#
#   def process_delete_subject(self):
#       try:
#           tong_tin_chi = 0
#           tong_diem = 0.0
#           for mon in self.view.sub_manager.list:
#               tin_chi = float(mon.credit)
#               diem_so = (float(mon.scoreProcess) * 0.3) + (float(mon.scoreMidterm) * 0.2) + (
#                           float(mon.scoreFinal) * 0.5)
#               tong_tin_chi += tin_chi
#               tong_diem += (diem_so * tin_chi)
#           gpa_cu = 0.0
#           if tong_tin_chi > 0:
#               gpa_cu = tong_diem / tong_tin_chi
#           path = f"../datasets/{self.current_acc}_gpa_user.json"
#           with open(path, "w", encoding="utf-8") as f:
#               json.dump({"gpa_ky_truoc": gpa_cu}, f, indent=4)
#       except Exception as e:
#           pass
#
#
#       Subname = self.view.NameLineEdit.text()
#       if Subname == "":
#           QMessageBox.critical(self.view.MainWindow, "Lỗi xóa", "Bạn phải chọn một môn học để xóa!")
#           return
#       dlg = QMessageBox.question(
#           self.view.MainWindow,
#           "Xác nhận xóa",
#           f"Bạn có chắc chắn muốn xóa môn [{Subname}] không?",
#           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
#       if dlg == QMessageBox.StandardButton.Yes:
#           ret = self.sub_manager.delete_item(Subname)
#           if ret:
#               self.sub_manager.export_json(self.file_subject)
#               self.display_subjects()
#               self.clear_inputs()
#               QMessageBox.information(self.view.MainWindow, "Thông báo", "Đã xóa thành công!")
#           else:
#               QMessageBox.warning(self.view.MainWindow, "Lỗi", "Không tìm thấy môn học trong dữ liệu!")
#
#
#   def search_subject(self):
#       keyword = self.view.lineEditTimmon.text().strip().lower()
#       # Lọc danh sách môn học khớp với từ khóa
#       filtered_list = [item for item in self.sub_manager.list if keyword in item.Subname.lower()]
#       self.display_subjects(filtered_list)
import sys
import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QHBoxLayout, QLineEdit, QPushButton, QWidget

# =====================================================================
# ⚠️ LƯU Ý QUAN TRỌNG:
# Hãy sửa lại đường dẫn import 2 dòng dưới đây sao cho khớp với
# thư mục chứa class Subject và Subjects trong project của bạn nhé!
# =====================================================================
import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QHBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox

# =====================================================================
# Hãy đảm bảo import file subject đúng với project của bạn
# =====================================================================
from model.subject import Subject
from model.subjects import Subjects


class AcademicController:
    def __init__(self, ui):
        self.ui = ui

        # 1. Khởi tạo dữ liệu
        self.ds_mon_hoc = Subjects()
        # self.ds_mon_hoc.import_json() # Mở ra nếu có file json

        # 2. Quản lý danh sách các hàng nhập điểm (3 hàng mặc định từ UI)
        self.danh_sach_cot_diem = [
            {'name': self.ui.txtcot1, 'weight': self.ui.txttrongso1, 'score': self.ui.txtdiem1, 'widget': None},
            {'name': self.ui.txtcot2, 'weight': self.ui.txttrongso2, 'score': self.ui.txtdiem2, 'widget': None},
            {'name': self.ui.txtcot3, 'weight': self.ui.txttrongso3, 'score': self.ui.txtdiem3, 'widget': None}
        ]

        # 3. Kết nối tín hiệu các nút bấm
        self.setup_signals()

        # 4. Load bảng lần đầu
        self.load_table_data()

        # 5. Kích hoạt tính trọng số lần đầu
        self.tinh_tong_trong_so()

    def setup(self):
        """Hàm trống để đề phòng file MainWindowEx gọi lệnh setup() không bị lỗi"""
        pass

    # ================= 1. KẾT NỐI SỰ KIỆN (SIGNALS) =================

    def setup_signals(self):
        # --- CÁC NÚT BẤM CHÍNH ---
        self.ui.pushButtonAddSubject.clicked.connect(self.them_mon_hoc)
        self.ui.pushButtonCalculateGPA.clicked.connect(self.tinh_gpa_tu_form)
        self.ui.btnthemcotdiemmoi.clicked.connect(self.them_cot_diem_moi)
        self.ui.pushButtonDelete.clicked.connect(self.xoa_mon_hoc)
        self.ui.pushButtonEdit.clicked.connect(self.sua_mon_hoc)

        # --- SỰ KIỆN COMBOBOX ---
        self.ui.comboboxcautrucdiem.currentIndexChanged.connect(self.thay_doi_cau_truc_diem)

        # --- SỰ KIỆN CLICK VÀO BẢNG (Để xem điểm, xếp loại) ---
        self.ui.tableWidgetthongtinmon.itemSelectionChanged.connect(self.chon_mon_tren_bang)

        # --- SỰ KIỆN TÌM KIẾM ---
        self.ui.lineEditTimmon.textChanged.connect(self.load_table_data)

        # --- SỰ KIỆN GÕ TRỌNG SỐ ---
        for row in self.danh_sach_cot_diem:
            row['weight'].textChanged.connect(self.tinh_tong_trong_so)

    # ================= 2. XỬ LÝ TRỌNG SỐ, COMBOBOX VÀ CỘT ĐIỂM ĐỘNG =================

    def thay_doi_cau_truc_diem(self):
        """Tự động điền Tên cột và Trọng số theo Combobox"""
        text = self.ui.comboboxcautrucdiem.currentText()

        # 1. Dọn dẹp: Xóa các hàng động dư thừa
        while len(self.danh_sach_cot_diem) > 3:
            row_to_remove = self.danh_sach_cot_diem[-1]
            self.xoa_cot_diem(row_to_remove)

        # 2. Xóa trắng toàn bộ dữ liệu hiện tại
        for row in self.danh_sach_cot_diem:
            row['name'].clear();
            row['weight'].clear();
            row['score'].clear()

        # 3. Điền dữ liệu theo mẫu
        if "30-20-50" in text:
            self.danh_sach_cot_diem[0]['name'].setText("Quá trình");
            self.danh_sach_cot_diem[0]['weight'].setText("30")
            self.danh_sach_cot_diem[1]['name'].setText("Giữa kì");
            self.danh_sach_cot_diem[1]['weight'].setText("20")
            self.danh_sach_cot_diem[2]['name'].setText("Cuối kì");
            self.danh_sach_cot_diem[2]['weight'].setText("50")

        elif "50-50" in text:
            self.danh_sach_cot_diem[0]['name'].setText("Quá trình");
            self.danh_sach_cot_diem[0]['weight'].setText("50")
            self.danh_sach_cot_diem[1]['name'].setText("Cuối kì");
            self.danh_sach_cot_diem[1]['weight'].setText("50")

        elif "30-70" in text:
            self.danh_sach_cot_diem[0]['name'].setText("Quá trình");
            self.danh_sach_cot_diem[0]['weight'].setText("30")
            self.danh_sach_cot_diem[1]['name'].setText("Cuối kì");
            self.danh_sach_cot_diem[1]['weight'].setText("70")

    def tinh_tong_trong_so(self):
        """Tính tổng % trọng số realtime"""
        tong = 0.0
        for row in self.danh_sach_cot_diem:
            try:
                val = float(row['weight'].text()) if row['weight'].text().strip() else 0.0
                tong += val
            except ValueError:
                pass

        self.ui.labletongtrongso.setText(f"{tong}%")
        if tong == 100.0:
            self.ui.labletongtrongso.setStyleSheet("color: green; font-weight: bold;")
            self.hien_thong_bao("Trọng số hợp lệ (100%)", is_error=False)
        else:
            self.ui.labletongtrongso.setStyleSheet("color: red; font-weight: bold;")
            self.hien_thong_bao(f"Cảnh báo: Tổng trọng số đang {tong}%", is_error=True)

    def them_cot_diem_moi(self):
        """Thêm hàng nhập điểm tùy chỉnh (Quiz, Chuyên cần...)"""
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)

        txt_name = QLineEdit();
        txt_name.setPlaceholderText("Tên cột (VD: Quiz 1)")
        txt_weight = QLineEdit();
        txt_weight.setPlaceholderText("Trọng số (%)")
        txt_score = QLineEdit();
        txt_score.setPlaceholderText("Điểm")
        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold;")

        row_layout.addWidget(txt_name);
        row_layout.addWidget(txt_weight);
        row_layout.addWidget(txt_score);
        row_layout.addWidget(btn_delete)

        scroll_layout = self.ui.scrollAreaWidgetContents.layout()
        if scroll_layout:
            insert_index = scroll_layout.count() - 1 if scroll_layout.count() > 0 else 0
            scroll_layout.insertWidget(insert_index, row_widget)

        new_row_dict = {'name': txt_name, 'weight': txt_weight, 'score': txt_score, 'widget': row_widget}
        self.danh_sach_cot_diem.append(new_row_dict)

        txt_weight.textChanged.connect(self.tinh_tong_trong_so)
        btn_delete.clicked.connect(lambda: self.xoa_cot_diem(new_row_dict))

    def xoa_cot_diem(self, row_dict):
        self.danh_sach_cot_diem.remove(row_dict)
        row_dict['widget'].deleteLater()
        self.tinh_tong_trong_so()

    # ================= 3. XỬ LÝ LẤY DỮ LIỆU & TÍNH TOÁN =================

    def lay_du_lieu_tu_form(self):
        ten_mon = self.ui.txttenmon.text().strip()
        if not ten_mon:
            self.hien_thong_bao("Lỗi: Tên môn không được để trống!", True)
            return None

        try:
            tin_chi = int(self.ui.txtsotinchi.text() or 0)
            if float(self.ui.labletongtrongso.text().replace("%", "")) != 100.0:
                self.hien_thong_bao("Lỗi: Không thể lưu khi tổng trọng số khác 100%!", True)
                return None

            components = []
            for row in self.danh_sach_cot_diem:
                if row['weight'].text().strip() and row['name'].text().strip():
                    name = row['name'].text().strip()
                    weight = float(row['weight'].text())
                    score = float(row['score'].text() or 0)
                    components.append({"name": name, "weight": weight, "score": score})

            return ten_mon, tin_chi, components
        except ValueError:
            self.hien_thong_bao("Lỗi: Tín chỉ, Trọng số và Điểm phải là SỐ!", True)
            return None

    def tinh_gpa_tu_form(self):
        data = self.lay_du_lieu_tu_form()
        if data:
            mon_tam = Subject(data[0], data[1], data[2])
            self.ui.lineEditGPA.setText(str(mon_tam.tinh_diem_gpa()))
            self.ui.lineEditXeploai.setText(mon_tam.tinh_xep_loai())
            self.hien_thong_bao("Đã tính thành công!", False)

    # ================= 4. THÊM, SỬA, XÓA & QUẢN LÝ BẢNG ĐỘNG =================

    def them_mon_hoc(self):
        data = self.lay_du_lieu_tu_form()
        if data:
            ten_mon, tin_chi, components = data

            # Kiểm tra môn đã tồn tại chưa (nếu có thì cập nhật)
            mon_cu = self.ds_mon_hoc.find_item(ten_mon)
            if mon_cu:
                self.ds_mon_hoc.list.remove(mon_cu)

            mon_moi = Subject(ten_mon, tin_chi, components)
            self.ds_mon_hoc.add_item(mon_moi)

            self.load_table_data()
            self.hien_thong_bao(f"Đã lưu môn: {ten_mon}!", False)

            # Xóa form
            self.ui.txttenmon.clear();
            self.ui.txtsotinchi.clear()
            for row in self.danh_sach_cot_diem: row['score'].clear()

    def xoa_mon_hoc(self):
        selected = self.ui.tableWidgetthongtinmon.selectedItems()
        if not selected:
            self.hien_thong_bao("Hãy chọn 1 môn trên bảng để xóa!", True)
            return

        ten_mon = self.ui.tableWidgetthongtinmon.item(selected[0].row(), 0).text()
        mon_can_xoa = self.ds_mon_hoc.find_item(ten_mon)
        if mon_can_xoa:
            self.ds_mon_hoc.list.remove(mon_can_xoa)
            self.load_table_data()
            self.hien_thong_bao(f"Đã xóa môn: {ten_mon}", False)

    def sua_mon_hoc(self):
        """Lấy dữ liệu từ bảng đổ ngược lên form để sửa"""
        selected = self.ui.tableWidgetthongtinmon.selectedItems()
        if not selected:
            self.hien_thong_bao("Hãy chọn 1 môn trên bảng để sửa!", True)
            return

        ten_mon = self.ui.tableWidgetthongtinmon.item(selected[0].row(), 0).text()
        mon_hoc = self.ds_mon_hoc.find_item(ten_mon)

        if mon_hoc:
            self.ui.txttenmon.setText(mon_hoc.Subname)
            self.ui.txtsotinchi.setText(str(mon_hoc.credit))

            # Xóa các dòng tùy chỉnh hiện tại
            while len(self.danh_sach_cot_diem) > 3:
                self.xoa_cot_diem(self.danh_sach_cot_diem[-1])

            # Đổ dữ liệu điểm vào form
            for i, comp in enumerate(mon_hoc.components):
                if i >= len(self.danh_sach_cot_diem):
                    self.them_cot_diem_moi()  # Sinh thêm dòng nếu thiếu

                self.danh_sach_cot_diem[i]['name'].setText(comp['name'])
                self.danh_sach_cot_diem[i]['weight'].setText(str(comp['weight']))
                self.danh_sach_cot_diem[i]['score'].setText(str(comp['score']))

            self.hien_thong_bao("Đã nạp dữ liệu. Hãy sửa và bấm Add Subject để lưu đè!", False)

    def chon_mon_tren_bang(self):
        selected = self.ui.tableWidgetthongtinmon.selectedItems()
        if not selected: return
        ten_mon = self.ui.tableWidgetthongtinmon.item(selected[0].row(), 0).text()
        mon_hoc = self.ds_mon_hoc.find_item(ten_mon)
        if mon_hoc:
            self.ui.lineEditGPA.setText(str(mon_hoc.tinh_diem_gpa()))
            self.ui.lineEditXeploai.setText(mon_hoc.tinh_xep_loai())

    def load_table_data(self):
        """Tự động sinh tiêu đề cột dựa trên dữ liệu người dùng nhập"""
        try:
            tu_khoa = self.ui.lineEditTimmon.text().strip().lower()
            danh_sach_loc = [mon for mon in self.ds_mon_hoc.list if tu_khoa in mon.Subname.lower()]

            # 1. Quét tìm tất cả TÊN CỘT ĐIỂM ĐỘC NHẤT
            unique_columns = []
            for mon in danh_sach_loc:
                for c in mon.components:
                    ten_cot = c['name'].strip()
                    if ten_cot not in unique_columns and ten_cot != "":
                        unique_columns.append(ten_cot)

            # 2. Tạo Header động cho bảng
            headers = ["Tên môn", "Số tín chỉ"] + unique_columns
            self.ui.tableWidgetthongtinmon.clear()  # Xóa sạch bảng cũ
            self.ui.tableWidgetthongtinmon.setColumnCount(len(headers))
            self.ui.tableWidgetthongtinmon.setHorizontalHeaderLabels(headers)
            self.ui.tableWidgetthongtinmon.setRowCount(len(danh_sach_loc))

            # 3. Đổ dữ liệu vào đúng vị trí cột
            for row_idx, mon in enumerate(danh_sach_loc):
                self.ui.tableWidgetthongtinmon.setItem(row_idx, 0, QTableWidgetItem(mon.Subname))
                self.ui.tableWidgetthongtinmon.setItem(row_idx, 1, QTableWidgetItem(str(mon.credit)))

                for c in mon.components:
                    ten_cot = c['name'].strip()
                    diem = str(c['score'])
                    if ten_cot in unique_columns:
                        # Tìm vị trí cột tương ứng (+2 vì bỏ qua Tên môn và Tín chỉ)
                        col_idx = unique_columns.index(ten_cot) + 2
                        self.ui.tableWidgetthongtinmon.setItem(row_idx, col_idx, QTableWidgetItem(diem))

            # Căn chỉnh độ rộng cột tự động cho đẹp
            self.ui.tableWidgetthongtinmon.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch)

        except AttributeError:
            pass

    def hien_thong_bao(self, text, is_error=False):
        try:
            self.ui.lablethongbao.setText(text)
            self.ui.lablethongbao.setStyleSheet(f"color: {'red' if is_error else 'green'}; font-weight: bold;")
        except AttributeError:
            print(f"THÔNG BÁO: {text}")
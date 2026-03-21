import datetime
import os

# Gom toàn bộ import của PyQt6 lại cho gọn
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from model.balances import Balances
from model.expense import Expense
from model.expenses import Expenses


class FinanceController:
    def __init__(self, main_view):
        self.view = main_view
        self.expense_manager = Expenses()
        self.balance_manager = Balances()
        self.editing_index = None  # Dùng để phân biệt trạng thái Thêm mới hay Sửa

    def setup(self):
        self.file_expense = f"../datasets/{self.current_acc}_expenses.json"
        self.file_balance = f"../datasets/{self.current_acc}_balance.json"

        # Khởi tạo file nếu chưa tồn tại
        if not os.path.exists(self.file_expense):
            with open(self.file_expense, "w", encoding="utf-8") as f: f.write("[]")
        if not os.path.exists(self.file_balance):
            with open(self.file_balance, "w", encoding="utf-8") as f: f.write('{"current_balance": 0}')

        self.expense_manager.load_json(self.file_expense)
        self.balance_manager.load_json(self.file_balance)

        # Khởi tạo giao diện ban đầu
        self.TAB3_REFRESH_ALL_UI()

        # Kết nối Signal & Slot
        self.view.pushButton_delete.clicked.connect(self.process_delete)
        self.view.pushButton_edit.clicked.connect(self.process_edit)
        self.view.pushButton_BieuDo.clicked.connect(self.show_pie_chart)

        # Lưu lại style và text gốc của nút Add Expense
        self.original_btn_style = self.view.pushButtonAddExpense.styleSheet()
        self.original_btn_text = self.view.pushButtonAddExpense.text()

    # =====================================================================
    # HÀM BỔ TRỢ: GOM CÁC BƯỚC CẬP NHẬT GIAO DIỆN VÀO 1 CHỖ CHO TỐI ƯU
    # =====================================================================
    def TAB3_REFRESH_ALL_UI(self):
        self.TAB3_UPDATE_TABLE_EXPENSE()
        self.TAB3_UPDATE_BALANCE_UI()
        self.TAB3_UPDATE_TOTAL_AND_COMPARE()
        self.TAB3_PROCESS_RIGHT_TABLE()

    # =====================================================================
    # PHẦN I: ADD EXPENSE VÀ HIỂN THỊ
    # =====================================================================
    def TAB3_PROCESS_ADD(self):
        ten = self.view.lineEditKhoanchi.text().strip()
        tien_str = self.view.lineEditGiatri.text().strip()
        loai = self.view.comboBoxLoaigia.currentText()
        ghi_chu = self.view.lineEditGhichu.text().strip()

        if not ten or not tien_str:
            QMessageBox.warning(self.view.MainWindow, "Thiếu thông tin", "Vui lòng nhập tên khoản chi và số tiền!")
            return

        try:
            tien = int(tien_str.replace(".", "").replace(",", ""))
            if tien <= 0:
                QMessageBox.warning(self.view.MainWindow, "Lỗi nhập liệu", "Vui lòng nhập số tiền lớn hơn 0!")
                return

            # --- TRẠNG THÁI SỬA (EDIT) ---
            if self.editing_index is not None:
                old_item = self.expense_manager.items[self.editing_index]
                self.balance_manager.current_balance += old_item.so_tien - tien  # Hoàn tiền cũ, trừ tiền mới

                # Cập nhật thông tin
                old_item.khoan_chi = ten
                old_item.so_tien = tien
                old_item.danh_muc = loai
                old_item.ghi_chu = ghi_chu

                # Reset giao diện nút bấm
                self.editing_index = None
                self.view.pushButtonAddExpense.setText(self.original_btn_text)
                self.view.pushButtonAddExpense.setStyleSheet(self.original_btn_style)
                msg = "Đã cập nhật khoản chi!"

            # --- TRẠNG THÁI THÊM MỚI (ADD) ---
            else:
                new_item = Expense(ten, tien, loai, ghi_chu)
                self.expense_manager.add_item(new_item)
                self.balance_manager.current_balance -= tien
                msg = "Đã thêm khoản chi mới!"

            # --- LƯU FILE VÀ CẬP NHẬT UI CHUNG ---
            self.expense_manager.export_json(self.file_expense)
            self.balance_manager.export_json(self.file_balance)

            self.TAB3_CLEAR_INPUTS()
            self.TAB3_REFRESH_ALL_UI()
            QMessageBox.information(self.view.MainWindow, "Thành công", msg)

        except ValueError:
            QMessageBox.warning(self.view.MainWindow, "Lỗi nhập liệu", "Số tiền phải là con số!")

    def TAB3_UPDATE_TABLE_EXPENSE(self):
        table = self.view.tableExpenselist_3
        table.setRowCount(0)
        # Các khoản chi mới nhất hiển thị lên trên cùng
        for row_index, item in enumerate(reversed(self.expense_manager.items)):
            table.insertRow(row_index)
            table.setItem(row_index, 0, QTableWidgetItem(str(item.ngay)))
            table.setItem(row_index, 1, QTableWidgetItem(str(item.khoan_chi)))
            table.setItem(row_index, 2, QTableWidgetItem(f"{item.so_tien:,}"))  # Dùng f-string cho gọn
            table.setItem(row_index, 3, QTableWidgetItem(str(item.danh_muc)))
            table.setItem(row_index, 4, QTableWidgetItem(str(item.ghi_chu)))

    def TAB3_CLEAR_INPUTS(self):
        self.view.lineEditKhoanchi.clear()
        self.view.lineEditGiatri.clear()
        self.view.lineEditGhichu.clear()
        self.view.lineEditKhoanchi.setFocus()

    # =====================================================================
    # PHẦN II: SỐ DƯ & THÊM THU NHẬP
    # =====================================================================
    def TAB3_UPDATE_BALANCE_UI(self):
        self.view.label_soduhientai.setText(f"{self.balance_manager.current_balance:,.0f} đ")

    def TAB3_PROCESS_ADD_INCOME(self):
        tien_nhap = self.view.lineEditIncome.text().strip()
        if not tien_nhap: return
        try:
            tien = int(tien_nhap.replace(".", "").replace(",", ""))
            if tien <= 0:
                QMessageBox.warning(self.view.MainWindow, "Lỗi nhập liệu", "Vui lòng nhập số tiền lớn hơn 0!")
                return
            self.balance_manager.current_balance += tien
            self.balance_manager.export_json(self.file_balance)

            self.TAB3_UPDATE_BALANCE_UI()
            self.view.lineEditIncome.clear()
            QMessageBox.information(self.view.MainWindow, "Ting Ting!", f"Đã nạp thêm {tien:,} đ vào tài khoản.")
        except ValueError:
            QMessageBox.warning(self.view.MainWindow, "Lỗi", "Vui lòng nhập số tiền hợp lệ!")

    # =====================================================================
    # PHẦN III: TỔNG CHI TIÊU & SO SÁNH THÁNG TRƯỚC
    # =====================================================================
    def TAB3_UPDATE_TOTAL_AND_COMPARE(self):
        today = datetime.datetime.now()
        cur_m, cur_y = today.month, today.year
        prev_m, prev_y = (12, cur_y - 1) if cur_m == 1 else (cur_m - 1, cur_y)

        total_current_month = total_prev_month = 0

        for item in self.expense_manager.items:
            try:
                date_obj = datetime.datetime.strptime(item.ngay, "%d/%m/%Y")
                if date_obj.month == cur_m and date_obj.year == cur_y:
                    total_current_month += item.so_tien
                elif date_obj.month == prev_m and date_obj.year == prev_y:
                    total_prev_month += item.so_tien
            except ValueError:
                continue

        self.view.label_total_3.setText(f"{total_current_month:,.0f} đ")

        # Xử lý So sánh
        diff = total_current_month - total_prev_month
        if diff > 0:
            self.view.label_tanggiam.setText(f"Tăng {diff:,.0f} đ so với tháng trước")
            self.view.label_tanggiam.setStyleSheet("color: red; font-weight: bold;")
        elif diff < 0:
            self.view.label_tanggiam.setText(f"Giảm {abs(diff):,.0f} đ so với tháng trước")
            self.view.label_tanggiam.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.view.label_tanggiam.setText("Chưa có biến động so với tháng trước")
            self.view.label_tanggiam.setStyleSheet("color: black;")

    # =====================================================================
    # PHẦN IV: BẢNG BÊN PHẢI (TÌM KIẾM - LỌC - SẮP XẾP)
    # =====================================================================
    def TAB3_PROCESS_RIGHT_TABLE(self):
        current_list = self.expense_manager.items.copy()

        # Lọc theo keyword
        keyword = self.view.lineEdittimkhoanchi_3.text().strip()
        if keyword:
            current_list = [item for item in current_list if keyword in item.ngay]

        # Lọc theo danh mục
        category = self.view.comboBoxloc_2.currentText()
        if category and category.strip():
            current_list = [item for item in current_list if item.danh_muc == category]

        # Sắp xếp
        sort_mode = self.view.comboBoxsapxep_2.currentText()
        if sort_mode == "Tăng dần":
            current_list.sort(key=lambda x: x.so_tien, reverse=False)
        elif sort_mode == "Giảm dần":
            current_list.sort(key=lambda x: x.so_tien, reverse=True)
        else:
            current_list.reverse()  # Mặc định hiển thị mới nhất lên trên

        self.TAB3_DRAW_RIGHT_TABLE(current_list)

    def TAB3_DRAW_RIGHT_TABLE(self, data_list):
        table = self.view.tablelExpenseist2_3
        table.setRowCount(0)
        for row_index, item in enumerate(data_list):
            table.insertRow(row_index)
            table.setItem(row_index, 0, QTableWidgetItem(str(item.ngay)))
            table.setItem(row_index, 1, QTableWidgetItem(str(item.khoan_chi)))
            table.setItem(row_index, 2, QTableWidgetItem(f"{item.so_tien:,}"))
            table.setItem(row_index, 3, QTableWidgetItem(str(item.danh_muc)))

    # =====================================================================
    # CHỨC NĂNG: XÓA VÀ SỬA (DELETE & EDIT)
    # =====================================================================
    def process_delete(self):
        try:
            if not hasattr(self.view, 'tableExpenselist_3'): return
            current_row = self.view.tableExpenselist_3.currentRow()

            if current_row < 0:
                QMessageBox.warning(self.view.MainWindow, "Chưa chọn dòng", "Vui lòng chọn một dòng để xóa!")
                return
            if not self.expense_manager.items:
                return

            reply = QMessageBox.question(self.view.MainWindow, 'Xác nhận',
                                         "Bạn có chắc muốn xóa khoản này?\n(Tiền sẽ được hoàn lại vào ví)",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Tính vị trí thực (vì bảng đang hiển thị ngược chiều list)
                real_index = len(self.expense_manager.items) - 1 - current_row
                item = self.expense_manager.items.pop(real_index)

                # Hoàn tiền
                self.balance_manager.current_balance += int(item.so_tien)

                self.expense_manager.export_json(self.file_expense)
                self.balance_manager.export_json(self.file_balance)

                # Gọi 1 hàm duy nhất thay vì 4 hàm rời rạc
                self.TAB3_REFRESH_ALL_UI()
                QMessageBox.information(self.view.MainWindow, "Thành công", "Đã xóa và hoàn tiền!")

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view.MainWindow, "Lỗi", f"Chi tiết lỗi: {str(e)}")

    def process_edit(self):
        if not hasattr(self.view, 'tableExpenselist_3'): return
        current_row = self.view.tableExpenselist_3.currentRow()

        if current_row < 0:
            QMessageBox.warning(self.view.MainWindow, "Chưa chọn dòng", "Vui lòng chọn dòng để sửa!")
            return

        real_index = len(self.expense_manager.items) - 1 - current_row
        self.editing_index = real_index
        item = self.expense_manager.items[real_index]

        # Đẩy dữ liệu lên UI
        self.view.lineEditKhoanchi.setText(item.khoan_chi)
        self.view.lineEditGiatri.setText(str(item.so_tien))
        self.view.comboBoxLoaigia.setCurrentText(item.danh_muc)
        self.view.lineEditGhichu.setText(item.ghi_chu)

        self.view.pushButtonAddExpense.setText("Lưu sửa đổi")
        self.view.pushButtonAddExpense.setStyleSheet("""
            QPushButton { background-color: #FF9800; color: white; }
            QPushButton:hover { background-color: #F57C00; }
        """)
        self.view.lineEditKhoanchi.setFocus()

    # =====================================================================
    # PHẦN V: BIỂU ĐỒ TRÒN MATPLOTLIB
    # =====================================================================
    def show_pie_chart(self):
        app_bg_color = '#FBF3E4'
        app_text_color = '#5D4037'
        app_colors = ['#E5A88B', '#E8D595', '#A3D1A3', '#A4C6DE', '#C1B4D8', '#E6A8A8']

        category_totals = {}
        total_amount = 0

        for item in self.expense_manager.items:
            category_totals[item.danh_muc] = category_totals.get(item.danh_muc, 0) + item.so_tien
            total_amount += item.so_tien

        if total_amount == 0:
            QMessageBox.information(self.view.MainWindow, "Thông báo", "Chưa có dữ liệu chi tiêu để vẽ biểu đồ!")
            return

        labels = [cat for cat, amt in category_totals.items() if amt > 0]
        sizes = [amt for amt in category_totals.values() if amt > 0]

        dialog = QDialog(self.view.MainWindow)
        dialog.setWindowTitle("Biểu Đồ Phân Tích Chi Tiêu")
        dialog.resize(700, 500)
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        fig, ax = plt.subplots(figsize=(6, 6))
        fig.set_facecolor(app_bg_color)
        ax.set_facecolor(app_bg_color)
        ax.set_title("TỶ LỆ CHI TIÊU THEO DANH MỤC", fontsize=14, fontweight='bold', pad=20, color=app_text_color)

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=app_colors,
               wedgeprops={'edgecolor': app_text_color}, textprops={'color': app_text_color, 'fontsize': 10})
        ax.axis('equal')

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        dialog.exec()
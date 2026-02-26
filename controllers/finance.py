# Phần I: add expense và hiênr thị ở bảng expense list ở frame bên trái:
import datetime

from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from model.balances import Balances
from model.expense import Expense
from model.expenses import Expenses


class FinanceController:
    def __init__(self, main_view):
        self.view = main_view
        self.expense_manager=Expenses()
        self.balance_manager = Balances()

    def setup(self):
        self.expense_manager.load_json("../datasets/expenses.json")  # Load lại dữ liệu cũ.
        self.TAB3_UPDATE_TABLE_EXPENSE()

        # ---KHỞI TẠO QUẢN LÝ SỐ DƯ PHẦN II ---
        self.balance_manager.load_json("../datasets/balance.json")
        self.TAB3_UPDATE_BALANCE_UI()

        # -- TÍNH TOÀN KHOẢN CHI VÀ SO SÁNH VS THÁNG TRƯỚC---
        self.TAB3_UPDATE_TOTAL_AND_COMPARE()

        # --- PHẦN IV: TÌM KIẾM, SẮP XẾP, LỌC ---
        self.TAB3_PROCESS_RIGHT_TABLE()
        
    def TAB3_PROCESS_ADD(self):  # Xử lý khi bấm nút Add Expense
        ten = self.view.lineEditKhoanchi.text().strip()
        tien_str = self.view.lineEditGiatri.text().strip()
        loai = self.view.comboBoxLoaigia.currentText()
        ghi_chu = self.view.lineEditGhichu.text().strip()
        # Kiểm tra dữ liệucó hợp lệ ko
        if not ten or not tien_str:
            QMessageBox.warning(self.view.MainWindow, "Thiếu thông tin", "Vui lòng nhập tên khoản chi và số tiền!")
            return
        try:
            tien = int(tien_str.replace(".", "").replace(",", ""))
            new_item = Expense(ten, tien, loai, ghi_chu)
            self.expense_manager.add_item(new_item)
            self.expense_manager.export_json("../datasets/expenses.json")
            # TRỪ TIỀN TRONG VÍ (liên quan phânf II)
            self.balance_manager.current_balance -= tien
            self.balance_manager.export_json("../datasets/balance.json")
            # Cập nhật lại bảng và xóa trắng ô nhập, cập nhật số dư ( PHẦN II):
            self.TAB3_UPDATE_TABLE_EXPENSE()
            self.TAB3_CLEAR_INPUTS()
            self.TAB3_UPDATE_BALANCE_UI()  # Cập nhật số dư mới bị trừ
            # Cập nhật lại tổng chi tiêu và so sánh với tháng trước
            self.TAB3_UPDATE_TOTAL_AND_COMPARE()
            self.TAB3_PROCESS_RIGHT_TABLE()  # Cập nhật bảng phải khi có dữ liệu mới
            QMessageBox.information(self.view.MainWindow, "Thành công", "Đã thêm khoản chi mới!")
        except ValueError:
            QMessageBox.warning(self.view.MainWindow, "Lỗi nhập liệu", "Số tiền phải là con số!")


    def TAB3_UPDATE_TABLE_EXPENSE(self):  # Hiển thị danh sách lên bảng tableExpenselist_3
        # logic: các khoản chi mới nhất sẽ hiển thị lên trên cùng.
        table = self.view.tableExpenselist_3
        table.setRowCount(0)
        data_list = self.expense_manager.items
        for row_index, item in enumerate(reversed(data_list)):
            table.insertRow(row_index)
            # Cột 0:Ngày
            table.setItem(row_index, 0, QTableWidgetItem(str(item.ngay)))
            # Cột 1:Tên khoản chi
            table.setItem(row_index, 1, QTableWidgetItem(str(item.khoan_chi)))
            # Cột 2:Số tiền(có dấu phẩy ngăn cách)
            money_str = "{:,}".format(item.so_tien)
            table.setItem(row_index, 2, QTableWidgetItem(money_str))
            # Cột 3:Danh mục
            table.setItem(row_index, 3, QTableWidgetItem(str(item.danh_muc)))
            # Cột 4:Ghi chú
            table.setItem(row_index, 4, QTableWidgetItem(str(item.ghi_chu)))


    def TAB3_CLEAR_INPUTS(self):  # Xóa trắng các ô nhập liệu
        self.view.lineEditKhoanchi.clear()
        self.view.lineEditGiatri.clear()
        self.view.lineEditGhichu.clear()
        self.view.lineEditKhoanchi.setFocus()  # Đưa con trỏ chuột quay lại ô đầu tiên


    # Phần 2: Phần hiển thị số dư, thêm thu nhập mới, trừ đi khoản chi.
    def TAB3_UPDATE_BALANCE_UI(self):  # Hàm cập nhật hiển thị số dư lên label_soduhientai
        money_str = "{:,.0f} đ".format(self.balance_manager.current_balance)
        self.view.label_soduhientai.setText(money_str)


    def TAB3_PROCESS_ADD_INCOME(self):  # Xử lý khi bấm nút Add Income (Thêm thu nhập)
        tien_nhap = self.view.lineEditIncome.text().strip()
        if not tien_nhap:
            return
        try:
            tien = int(tien_nhap.replace(".", "").replace(",", ""))
            self.balance_manager.current_balance += tien
            self.balance_manager.export_json("../datasets/balance.json")
            # Cập nhật lại giao diện
            self.TAB3_UPDATE_BALANCE_UI()
            self.view.lineEditIncome.clear()
            QMessageBox.information(self.view.MainWindow, "Ting Ting!", f"Đã nạp thêm {tien:,} đ vào tài khoản.")
        except ValueError:
            QMessageBox.warning(self.view.MainWindow, "Lỗi", "Vui lòng nhập số tiền hợp lệ!")


    # PHẦN III: XỬ LÍ HIỂN THỊ VÀ SO SÁNH TỔNG CHI TIÊU SO VỚI THÁNG TRƯỚC.
    def TAB3_UPDATE_TOTAL_AND_COMPARE(self):  # Tính tổng chi tiêu tháng này và so sánh với tháng trước
        # Xác định thời gian hiện tại
        today = datetime.datetime.now()
        current_month = today.month
        current_year = today.year
        # Xác định tháng trước
        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year
        # Tính toán từ danh sách expenses
        total_current_month = 0
        total_prev_month = 0
        for item in self.expense_manager.items:
            try:
                # Chuyển chuỗi thành ngày tháng
                date_obj = datetime.datetime.strptime(item.ngay, "%d/%m/%Y")
                if date_obj.month == current_month and date_obj.year == current_year:
                    total_current_month += item.so_tien
                # + tháng trước nếu ko khớp
                elif date_obj.month == prev_month and date_obj.year == prev_year:
                    total_prev_month += item.so_tien
            except ValueError:
                continue  # Bỏ qua nếu lỗi ngày tháng
        # Hiển thị Tổng chi tiêu tháng này lên label_total_3
        self.view.label_total_3.setText(f"{total_current_month:,.0f} đ")
        # Xử lý logic So sánh Tăng/Giảm
        diff = total_current_month - total_prev_month
        if diff > 0:  # Chi nhiều hơn tháng trước-> Màu Đỏ(Cảnh báo)
            self.view.label_tanggiam.setText(f"Tăng {diff:,.0f} đ so với tháng trước")
            self.view.label_tanggiam.setStyleSheet("color: red;font-weight:bold;")
        elif diff < 0:  # Chi ít hơn tháng trước-> Màu Xanh(Tốt)
            self.view.label_tanggiam.setText(f"Giảm {abs(diff):,.0f} đ so với tháng trước")
            self.view.label_tanggiam.setStyleSheet("color:green;font-weight: bold;")
        else:  # Bằng nhau hoặc tháng đầu tiên( lấy tháng 1 làm gốc) (diff = 0)
            self.view.label_tanggiam.setText("Chưa có biến động so với tháng trước")
            self.view.label_tanggiam.setStyleSheet("color: black;")


    # PHẦN IV: XỬ LÝ BẢNG BÊN PHẢI (TÌM KIẾM - SẮP XẾP - LỌC)
    def TAB3_PROCESS_RIGHT_TABLE(self):  # Hàm xử lý logic tổng hợp cho bảng bên phải
        current_list = self.expense_manager.items.copy()
        # XỬ LÝ TÌM KIẾM THEO NGÀY
        keyword = self.view.lineEdittimkhoanchi_3.text().strip()
        if keyword:
            current_list = [item for item in current_list if keyword in item.ngay]
        # XỬ LÝ LỌC DANH MỤC
        category = self.view.comboBoxloc_2.currentText()
        # Chỉ lọc nếu người dùng chọn một danh mục cụ thể(khác rỗng)
        if category and category.strip() != "":
            current_list = [item for item in current_list if item.danh_muc == category]
        # XỬ LÝ SẮP XẾP
        sort_mode = self.view.comboBoxsapxep_2.currentText()
        if sort_mode == "Tăng dần":
            current_list.sort(key=lambda x: x.so_tien, reverse=False)
        elif sort_mode == "Giảm dần":
            current_list.sort(key=lambda x: x.so_tien, reverse=True)
        else:
            current_list.reverse()
        # HIỂN THỊ RA BẢNG
        self.TAB3_DRAW_RIGHT_TABLE(current_list)


    def TAB3_DRAW_RIGHT_TABLE(self, data_list):
        table = self.view.tablelExpenseist2_3
        table.setRowCount(0)
        for row_index, item in enumerate(data_list):
            table.insertRow(row_index)
            table.setItem(row_index, 0, QTableWidgetItem(str(item.ngay)))
            table.setItem(row_index, 1, QTableWidgetItem(str(item.khoan_chi)))
            table.setItem(row_index, 2, QTableWidgetItem("{:,}".format(item.so_tien)))
            table.setItem(row_index, 3, QTableWidgetItem(str(item.danh_muc)))
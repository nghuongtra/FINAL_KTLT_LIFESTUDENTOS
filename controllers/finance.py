# Phần I: add expense và hiênr thị ở bảng expense list ở frame bên trái:
import datetime
import os

from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

#_______Vẽ Biểu đồ____________________________________________-
# 1. Thêm QDialog, QVBoxLayout của PyQt6:
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QVBoxLayout

# 2. Thêm thư viện matplotlib và công cụ nhúng vào Qt:
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
#____________________________________________-
from model.balances import Balances
from model.expense import Expense
from model.expenses import Expenses


class FinanceController:
    def __init__(self, main_view):
        self.view = main_view
        self.expense_manager=Expenses()
        self.balance_manager = Balances()
        self.editing_index = None # dùng cho kiểm tra đang thựuc hiện thao tác sửa hay thêm mới

    def setup(self):
        self.file_expense = f"../datasets/{self.current_acc}_expenses.json"
        self.file_balance = f"../datasets/{self.current_acc}_balance.json"
        if not os.path.exists(self.file_expense):
            with open(self.file_expense, "w", encoding="utf-8") as f: f.write("[]")
        if not os.path.exists(self.file_balance):
            with open(self.file_balance, "w", encoding="utf-8") as f: f.write('{"current_balance": 0}')
        self.expense_manager.load_json(self.file_expense)
        self.balance_manager.load_json(self.file_balance)
        self.TAB3_UPDATE_TABLE_EXPENSE()
        self.TAB3_UPDATE_BALANCE_UI()

        # -- TÍNH TOÀN KHOẢN CHI VÀ SO SÁNH VS THÁNG TRƯỚC---
        self.TAB3_UPDATE_TOTAL_AND_COMPARE()

        # --- PHẦN IV: TÌM KIẾM, SẮP XẾP, LỌC ---
        self.TAB3_PROCESS_RIGHT_TABLE()
        # --- Delete + edit---
        self.view.pushButton_delete.clicked.connect(self.process_delete)
        self.view.pushButton_edit.clicked.connect(self.process_edit)
        #_______________Vẽ biểu đồ____
        self.view.pushButton_BieuDo.clicked.connect(self.show_pie_chart)

        self.original_btn_style = self.view.pushButtonAddExpense.styleSheet()
        # Lưu lại chữ gốc ("+ Add Expense")
        self.original_btn_text= self.view.pushButtonAddExpense.text()
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
            # ========================Sửa=======================================
            if hasattr(self, 'editing_index') and self.editing_index is not None:
                old_item = self.expense_manager.items[self.editing_index]
                #Tính lại tiền trong ví (Cộng lại tiền cũ->Trừ đi tiền mới sửa)
                self.balance_manager.current_balance+=old_item.so_tien- tien
                #Cập nhật thông tin mới vào item đó
                old_item.khoan_chi=ten
                old_item.so_tien=tien
                old_item.danh_muc=loai
                old_item.ghi_chu=ghi_chu
                #Reset trạng thái về "Thêm mới"
                self.editing_index = None
                self.view.pushButtonAddExpense.setText(self.original_btn_text)  # Trả lại chữ "+ Add Expense"
                self.view.pushButtonAddExpense.setStyleSheet(self.original_btn_style)
                # Lưu file và cập nhật giao diện
                self.expense_manager.export_json(self.file_expense)
                self.balance_manager.export_json(self.file_balance)
                self.TAB3_UPDATE_TABLE_EXPENSE()
                self.TAB3_CLEAR_INPUTS()
                self.TAB3_UPDATE_BALANCE_UI()
                self.TAB3_UPDATE_TOTAL_AND_COMPARE()
                self.TAB3_PROCESS_RIGHT_TABLE()
                QMessageBox.information(self.view.MainWindow, "Thành công", "Đã cập nhật khoản chi!")
                return  # Dừng hàm tại đây để không chạy xuống phần Thêm Mới ở bên dưới
            # ========================================================================
            new_item = Expense(ten, tien, loai, ghi_chu)
            self.expense_manager.add_item(new_item)
            self.expense_manager.export_json(self.file_expense)
            # TRỪ TIỀN TRONG VÍ (liên quan phânf II)
            self.balance_manager.current_balance -= tien
            self.balance_manager.export_json(self.file_balance)
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
            self.balance_manager.export_json(self.file_balance)
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
# Thêm chức năng delete và edit cho bảng list
    def process_delete(self):
        try: #Kiểm tra thử xem bảng và view có tồn tại không
            if not hasattr(self.view, 'tableExpenselist_3'):
                return
            current_row = self.view.tableExpenselist_3.currentRow()
            #Kiểm tra dòng hợp lệ
            if current_row < 0:
                QMessageBox.warning(self.view.MainWindow, "Chưa chọn dòng", "Vui lòng chọn một dòng để xóa!")
                return
            #Kiểm tra danh sách có rỗng kh
            if not self.expense_manager.items:
                QMessageBox.warning(self.view.MainWindow, "Lỗi dữ liệu",
                                    "Danh sách chi tiêu đang trống, không thể xóa!")
                self.TAB3_UPDATE_TABLE_EXPENSE()
                return
            # xác nhận
            reply = QMessageBox.question(self.view.MainWindow, 'Xác nhận',
                                         "Bạn có chắc muốn xóa khoản này?\n(Tiền sẽ được hoàn lại vào ví)",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Tính toán chỉ số thực
                total_items=len(self.expense_manager.items)
                real_index=total_items - 1 - current_row
                # Kiểm tra chỉ số thực có nằm trong danh sách kh
                if real_index<0 or real_index>=total_items:
                    QMessageBox.critical(self.view.MainWindow, "Lỗi Nghiêm Trọng",
                                         f"Lỗi đồng bộ dữ liệu!\nIndex: {real_index}, Total: {total_items}")
                    self.TAB3_UPDATE_TABLE_EXPENSE()  # Vẽ lại bảng
                    return
                item = self.expense_manager.items[real_index]
                self.expense_manager.items.pop(real_index)
                # Cập nhật tiền
                if hasattr(item, 'so_tien'):
                    self.balance_manager.current_balance += int(item.so_tien)  # Đảm bảo là số int
                #Lưu file
                self.expense_manager.export_json(self.file_expense)
                self.balance_manager.export_json(self.file_balance)
                # Update giao diện
                self.TAB3_UPDATE_TABLE_EXPENSE()
                self.TAB3_UPDATE_BALANCE_UI()
                self.TAB3_UPDATE_TOTAL_AND_COMPARE()
                self.TAB3_PROCESS_RIGHT_TABLE()
                QMessageBox.information(self.view.MainWindow, "Thành công", "Đã xóa và hoàn tiền!")
        except Exception as e:
            # In lỗi chi tiết
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view.MainWindow, "Lỗi không mong muốn", f"Chi tiết lỗi: {str(e)}")

    def process_edit(self):
        # Kiểm tra dòng chọn
        if not hasattr(self.view, 'tableExpenselist_3'): return
        current_row=self.view.tableExpenselist_3.currentRow()
        if current_row< 0:
            QMessageBox.warning(self.view.MainWindow,"Chưa chọn dòng", "Vui lòng chọn dòng để sửa!")
            return
        # Tính vị trí thực
        real_index = len(self.expense_manager.items)-1-current_row
        # Đánh dấu là đang sửa dòng htai
        self.editing_index = real_index
        # Đẩy dữ liệu cũ lên form nhập liệu
        item = self.expense_manager.items[real_index]
        self.view.lineEditKhoanchi.setText(item.khoan_chi)
        self.view.lineEditGiatri.setText(str(item.so_tien))
        self.view.comboBoxLoaigia.setCurrentText(item.danh_muc)
        self.view.lineEditGhichu.setText(item.ghi_chu)
        # Đổi giao diện nút Add thành "Lưu sửa đổi"
        self.view.pushButtonAddExpense.setText("Lưu sửa đổi")
        self.view.pushButtonAddExpense.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800; 
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                """)
        self.view.lineEditKhoanchi.setFocus()

    # PHẦN V: XỬ LÝ VẼ BIỂU ĐỒ TRÒN BẰNG MATPLOTLIB (Đã đổi màu theo tone app)
    def show_pie_chart(self):
        # ĐỊNH NGHĨA TÔNG MÀU APP (Màu be ấm áp)
        # Lấy cảm hứng từ màu nền của các card
        app_bg_color = '#FBF3E4'

        # ĐỊNH NGHĨA MÀU VĂN BẢN (Nâu đậm ấm)
        app_text_color = '#5D4037'

        # ĐỊNH NGHĨA BẢNG MÀU MIẾNG GHÉP (Màu pastel ấm, hài hòa)
        # Danh sách 6 màu pastel tông ấm
        app_colors = [
            '#E5A88B',  # Pastel Orange
            '#E8D595',  # Pastel Yellow
            '#A3D1A3',  # Pastel Green
            '#A4C6DE',  # Pastel Blue
            '#C1B4D8',  # Pastel Purple
            '#E6A8A8',  # Pastel Pink
        ]

        # 1. Tính tổng tiền theo từng danh mục (Giữ nguyên logic dữ liệu)
        category_totals = {}
        total_amount = 0

        for item in self.expense_manager.items:
            cat = item.danh_muc
            category_totals[cat] = category_totals.get(cat, 0) + item.so_tien
            total_amount += item.so_tien

        if total_amount == 0:
            QMessageBox.information(self.view.MainWindow, "Thông báo", "Chưa có dữ liệu chi tiêu để vẽ biểu đồ!")
            return

        # 2. Chuẩn bị dữ liệu cho matplotlib (Giữ nguyên)
        labels = []
        sizes = []
        for cat, amount in category_totals.items():
            if amount > 0:
                labels.append(cat)
                sizes.append(amount)

        # 3. Tạo cửa sổ Popup (QDialog) và bố cục (Giữ nguyên)
        dialog = QDialog(self.view.MainWindow)
        dialog.setWindowTitle("Biểu Đồ Phân Tích Chi Tiêu")
        dialog.resize(700, 500)
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        # 4. Dùng Matplotlib để vẽ biểu đồ VỚI MÀU SẮC MỚI
        # Tạo Figure (bức tranh) và Axes (trục tọa độ)
        fig, ax = plt.subplots(figsize=(6, 6))

        # --- ĐỔI MÀU NỀN CỦA FIGURE VÀ AXES ---
        fig.set_facecolor(app_bg_color)
        ax.set_facecolor(app_bg_color)

        # --- ĐỔI MÀU TIÊU ĐỀ ---
        ax.set_title("TỶ LỆ CHI TIÊU THEO DANH MỤC", fontsize=14,
                     fontweight='bold', pad=20, color=app_text_color)

        # --- VẼ BIỂU ĐỒ VỚI BẢNG MÀU APP ---
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=app_colors,  # Sử dụng bảng màu ấm mới
               wedgeprops={'edgecolor': app_text_color},  # Thêm viền nâu mỏng cho sắc nét
               textprops={'color': app_text_color, 'fontsize': 10})  # Đổi màu chữ label

        # Đảm bảo biểu đồ tròn vo (Giữ nguyên)
        ax.axis('equal')

        # 5. Nhúng cái "Bức tranh" (Figure) của matplotlib vào PyQt6 (Giữ nguyên)
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Hiển thị cửa sổ popup lên (Giữ nguyên)
        dialog.exec()
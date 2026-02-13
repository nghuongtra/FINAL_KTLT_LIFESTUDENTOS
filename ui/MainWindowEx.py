from functools import partial
import datetime

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox,QPushButton,QTableWidgetItem

from model.comingevents import Upcomingevents
from model.task import Task
from model.tasks import Tasks
from ui.MainWindow import Ui_MainWindow
import ui.resources_rc

#Import TAB2
from model.subjects import Subjects
from model.subject import Subject

# IMPORT CỦA TAB 3: FINANCE MANAGEMENT:
from model.expense import Expense
from model.expenses import Expenses
from model.balances import Balances


from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTableWidgetItem
class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi((MainWindow))
        self.MainWindow = MainWindow
        self.tasks = Tasks()
        self.selectedTask=None
        self.tasks.import_json("../datasets/tasks.json")
        self.showTasksIntoQListWidget()

#TAB 2:
        self.sub_manager = Subjects()
        self.sub_manager.import_json("../datasets/subjects.json")
        self.display_subjects()

# --- TAB 3: Khởi tạo Finance ------------------
        # --- KHỞI TẠO DỮ LIỆU CHI TIÊU PHẦN I---
        self.expense_manager=Expenses()
        self.expense_manager.load_json("../datasets/expenses.json")#Load lại dữ liệu cũ.
        self.TAB3_UPDATE_TABLE_EXPENSE()

        #---KHỞI TẠO QUẢN LÝ SỐ DƯ PHẦN II ---
        self.balance_manager = Balances()
        self.balance_manager.load_json("../datasets/balance.json")
        self.TAB3_UPDATE_BALANCE_UI()

        #-- TÍNH TOÀN KHOẢN CHI VÀ SO SÁNH VS THÁNG TRƯỚC---
        self.TAB3_UPDATE_TOTAL_AND_COMPARE()

        #--- PHẦN IV: TÌM KIẾM, SẮP XẾP, LỌC ---
        self.TAB3_PROCESS_RIGHT_TABLE()

    def show(self):
        self.MainWindow.show()
        self.setupSignalAndSlot()
        self.stackedWidget.setCurrentIndex(0)
        self.updateCountdown()

    def setupSignalAndSlot(self):
        #liên kết các nút bấm trên header với các page
        self.pushButtonOverview.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButtonAcademic.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButtonFinanceManagement.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButtonTaskScheduler.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButtonInsights.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        #Overview
        self.pushButtonViewDetail.clicked.connect(self.process_viewdetail)
        self.pushButtonManageFinances.clicked.connect(self.process_managefinance)
        self.pushButtonViewCalendar.clicked.connect(self.process_calendar)
        self.pushButtonViewTask.clicked.connect(self.process_task)
        #Phần của tab task
        self.pushButtonNew.clicked.connect(self.processNew)
        self.pushButtonSave.clicked.connect(self.processSave)
        self.pushButtonDeleteTask.clicked.connect(self.processRemove)
        self.listWidgetTask.itemSelectionChanged.connect(self.processItemSelection)
        self.dateEditDeadline.dateChanged.connect(self.updateCountdown)
        self.timeEditDeadline.timeChanged.connect(self.updateCountdown)

#TAB 2:
        self.pushButtonCalculateGPA.clicked.connect(self.process_calculate_gpa)
        self.pushButtonAddSubject.clicked.connect(self.process_add_subject)
        self.pushButtonEdit.clicked.connect(self.process_edit_subject)
        self.pushButtonDelete.clicked.connect(self.process_delete_subject)
        self.tableWidgetthongtinmon.itemSelectionChanged.connect(self.process_selection)

        #TAB 3: FINANCE MANAGEMENT.
        self.pushButtonAddExpense.clicked.connect(self.TAB3_PROCESS_ADD) #PHẦN I
        self.pushButton_addincome.clicked.connect(self.TAB3_PROCESS_ADD_INCOME) #PHẦN II
        self.pushButtonsearch_3.clicked.connect(self.TAB3_PROCESS_RIGHT_TABLE)
        self.comboBoxsapxep_2.currentIndexChanged.connect(self.TAB3_PROCESS_RIGHT_TABLE)
        self.comboBoxloc_2.currentIndexChanged.connect(self.TAB3_PROCESS_RIGHT_TABLE)
#########Tab overview
    def process_viewdetail(self):
        total_credits = 0
        total_weighted_score_10 = 0
        for item in self.sub_manager.list:
                credit = int(item.credit)
                score_final = float(item.scoreFinal)
                total_credits += credit
                total_weighted_score_10 += (score_final * credit)
        if total_credits > 0:
            avgScore = total_weighted_score_10 / total_credits
            gpa_4 = (avgScore/ 10) * 4

            self.labelGPA.setText(f"{gpa_4:.2f}")
            self.labelGrade.setText(f"{avgScore:.2f}")
        else:
            self.labelGPA.setText("0.00")
            self.labelGrade.setText("Chưa có dữ liệu")

    def process_managefinance(self):
        total = self.label_total_3.text()
        self.labelTotal.setText(total)

    def process_calendar(self):
        now = datetime.datetime.now()
        day_month = now.strftime("%d/%m")
        today_display = now.strftime("%d/%m/%Y")
        ucvs = Upcomingevents()
        ucvs.import_json("../datasets/upcomingevents.json")
        event_today = "Không có sự kiện đặc biệt"
        for item in ucvs.list:
            if item.date_month == day_month:
                event_today = item.sukien
                break
        self.labelComingEvent.setText(f"Hôm nay: {today_display}\nSự kiện: {event_today}")

    def process_task(self):
        pending_count = 0
        overdue_count = 0
        now = datetime.datetime.now()
        for index in range(self.tasks.size()):
            task = self.tasks.item(index)

            if isinstance(task.deadline, str):
                task.deadline = datetime.date.fromisoformat(task.deadline)
            if isinstance(task.deadlinetime, str):
                task.deadlinetime = datetime.time.fromisoformat(task.deadlinetime)
            if not task.isfinish:
                pending_count += 1
                dt_deadline = datetime.datetime.combine(task.deadline, task.deadlinetime)
                if dt_deadline < now:
                    overdue_count += 1
        self.labelTaskPending.setText(str(pending_count))
        self.labelTaskOverdue.setText(str(overdue_count))
        if overdue_count > 0:
            self.labelTaskOverdue.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.labelTaskOverdue.setStyleSheet("color: green;")
#{ Phần của tab task scheduler
    def showTasksIntoQListWidget(self):
        self.listWidgetTask.clear()
        for index in range(self.tasks.size()):
            task = self.tasks.item(index)
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, task)
            item.setText(str(task))
            item.setCheckState(Qt.CheckState.Unchecked)
            if task.isfinish == True:
                item.setIcon(QIcon("../images/ic_finished.png"))
                item.setBackground(QColor("white"))
                item.setForeground(QColor("black"))
            else:
                item.setIcon(QIcon("../images/ic_notfinished.png"))
            if isinstance(task.deadline, str):
                task.deadline = datetime.date.fromisoformat(task.deadline)
            if isinstance(task.deadlinetime, str):
                task.deadlinetime = datetime.time.fromisoformat(task.deadlinetime)
            self.listWidgetTask.addItem(item)
            if not task.isfinish:
                dt_deadline = datetime.datetime.combine(task.deadline, task.deadlinetime)
                dt_now = datetime.datetime.now()
                diff = (dt_deadline - dt_now).total_seconds() #tính khoảng cách thời gian cho labelcountdown
                if diff < 0:
                    # QUÁ HẠN: Nền đỏ nhạt, chữ đỏ
                    item.setBackground(QColor("#FFCDD2"))
                    item.setForeground(QColor("#B71C1C"))
                elif diff <= 86400:
                    # GẤP: Nền vàng nhạt, chữ cam
                    item.setBackground(QColor("#FFF9C4"))
                    item.setForeground(QColor("#F57F17"))
                else:
                    item.setBackground(QColor("#E8F5E9"))

    def processNew(self):
        self.lineEditTitle.setText("")
        self.textEditContent.setText("")
        self.dateEditDeadline.setSpecialValueText(None)
        self.radioButtonFinished.setAutoExclusive(False)
        self.radioButtonNotFinished.setAutoExclusive(False)
        self.radioButtonFinished.setChecked(False)
        self.radioButtonNotFinished.setChecked(False)
        self.radioButtonFinished.setAutoExclusive(True)
        self.radioButtonNotFinished.setAutoExclusive(True)
        self.selectedTask = None
        self.lineEditTitle.setFocus()

    def processSave(self):
        title = self.lineEditTitle.text()
        content = self.textEditContent.toPlainText()
        date = self.dateEditDeadline.date().toPyDate()
        time = self.timeEditDeadline.time().toPyTime()
        isFinished = self.radioButtonFinished.isChecked()
        task = Task(title, content, date, time, isFinished)
        if self.selectedTask == None:
            self.tasks.add_item(task)
        else:
            index = self.tasks.index(self.selectedTask)
            self.tasks.update(index, task)
        self.selectedTask = task
        self.showTasksIntoQListWidget()
        self.tasks.export_json("../datasets/tasks.json")

    def processRemove(self):
        answer = QMessageBox.question(
            self.MainWindow,
            'Xác nhận',
            'Bạn có chắc chắn muốn xóa công việc này không?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.No:
            return
        size = self.listWidgetTask.count()
        for index in range(size - 1, -1, -1):
            item = self.listWidgetTask.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                self.tasks.removeByIndex(index)
        self.selectedTask = None
        self.showTasksIntoQListWidget()
        self.tasks.export_json("../datasets/tasks.json")

    def processItemSelection(self):
        row = self.listWidgetTask.currentRow()
        if row < 0:
            return
        task = self.tasks.item(row)
        self.lineEditTitle.setText(task.title)
        self.textEditContent.setText(task.content)
        self.dateEditDeadline.setDate(task.deadline)
        self.timeEditDeadline.setTime(task.deadlinetime)
        if task.isfinish:
            self.radioButtonFinished.setChecked(True)
            self.radioButtonNotFinished.setChecked(False)
        else:
            self.radioButtonFinished.setChecked(False)
            self.radioButtonNotFinished.setChecked(True)
        self.selectedTask = task
    def updateCountdown(self):
        q_date = self.dateEditDeadline.date()
        q_time = self.timeEditDeadline.time()
        deadline_qdt = QDateTime(q_date, q_time)
        now_qdt = QDateTime.currentDateTime()
        seconds_diff = now_qdt.secsTo(deadline_qdt)
        if seconds_diff < 0:
            self.labelCountdown.setText("Đã quá hạn!")
            self.labelCountdown.setStyleSheet("color: red; font-weight: bold;")
        else:
            days = seconds_diff // 86400
            hours = (seconds_diff % 86400) // 3600
            minutes = (seconds_diff % 3600) // 60
            self.labelCountdown.setText(f"Còn: {days} ngày, {hours} giờ, {minutes} phút")
            self.labelCountdown.setStyleSheet("color: blue; font-weight: bold;")

    # ===================================================================
    # LOGIC RIÊNG CHO TAB 2
    # ===================================================================

    def process_calculate_gpa(self):
        if self.NameLineEdit.text() == "" or self.ProcessLineEdit.text() == "":
            QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return
        ten = self.NameLineEdit.text()
        tin_chi = int(self.CreditLineEdit.text() or 0)
        qt = float(self.ProcessLineEdit.text() or 0)
        gk = float(self.MidtermLineEdit.text() or 0)
        ck = float(self.FinalLineEdit.text() or 0)

        # Tạo đối tượng tạm để tính toán
        temp_sub = Subject(ten, tin_chi, qt, gk, ck)

        # Hiển thị kết quả lên giao diện
        self.lineEditGPA.setText(str(temp_sub.tinh_diem_gpa()))
        self.lineEditXeploai.setText(temp_sub.tinh_xep_loai())

    def process_add_subject(self):
        Subname = self.NameLineEdit.text()
        credit = self.CreditLineEdit.text()
        process = self.ProcessLineEdit.text()
        midterm = self.MidtermLineEdit.text()
        final = self.FinalLineEdit.text()
        if Subname == "":
            QMessageBox.warning(self.MainWindow, "Lỗi", "Tên môn không được để trống!")
            return
        # 1. Kiểm tra xem môn này đã có chưa
        if self.sub_manager.find_item(Subname) is not None:
            QMessageBox.warning(self.MainWindow, "Lỗi",
                                f"Môn '{Subname}' đã tồn tại! Vui lòng dùng nút Edit")
            self.NameLineEdit.setText("")
            self.CreditLineEdit.setText("")
            self.ProcessLineEdit.setText("")
            self.MidtermLineEdit.setText("")
            self.FinalLineEdit.setText("")
            self.NameLineEdit.setFocus()
            return

        # Lưu file và cập nhật bảng
        item = Subject(Subname, credit, process, midterm, final)
        self.sub_manager.add_item(item)
        self.sub_manager.export_json()
        self.display_subjects()
        self.NameLineEdit.clear()
        self.CreditLineEdit.clear()
        self.ProcessLineEdit.clear()
        self.MidtermLineEdit.clear()
        self.FinalLineEdit.clear()
        QMessageBox.information(self.MainWindow, "Thông báo", "Đã thêm môn học mới thành công!")

    def display_subjects(self):
        self.tableWidgetthongtinmon.setRowCount(0)
        for item in self.sub_manager.list:
            row_index = self.tableWidgetthongtinmon.rowCount()
            self.tableWidgetthongtinmon.insertRow(row_index)
            self.tableWidgetthongtinmon.setItem(row_index, 0, QTableWidgetItem(str(item.Subname)))
            self.tableWidgetthongtinmon.setItem(row_index, 1, QTableWidgetItem(str(item.credit)))
            self.tableWidgetthongtinmon.setItem(row_index, 2, QTableWidgetItem(str(item.scoreProcess)))
            self.tableWidgetthongtinmon.setItem(row_index, 3, QTableWidgetItem(str(item.scoreMidterm)))
            self.tableWidgetthongtinmon.setItem(row_index, 4, QTableWidgetItem(str(item.scoreFinal)))

    def process_selection(self):
        selected_row = self.tableWidgetthongtinmon.currentRow()
        if selected_row < 0:
            return

        item = self.sub_manager.list[selected_row]
        self.NameLineEdit.setText(str(item.Subname))
        self.CreditLineEdit.setText(str(item.credit))
        self.ProcessLineEdit.setText(str(item.scoreProcess))
        self.MidtermLineEdit.setText(str(item.scoreMidterm))
        self.FinalLineEdit.setText(str(item.scoreFinal))
        self.lineEditGPA.setText("")
        self.lineEditXeploai.setText("")

    def process_edit_subject(self):
        Subname = self.NameLineEdit.text()
        if Subname == "":
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn môn cần sửa!")
            return

        # 1. Tìm môn học trong danh sách dựa theo tên
        # (Lưu ý: Tên môn coi như là ID, không được sửa tên ở đây)
        existing_sub = self.sub_manager.find_item(Subname)

        if existing_sub is None:
            QMessageBox.warning(self.MainWindow, "Lỗi",
                                f"Không tìm thấy môn '{Subname}' để sửa! Vui lòng dùng nút Thêm (Add).")
            return

        # 2. Cập nhật thông tin mới vào đối tượng tìm thấy
        try:
            existing_sub.credit = int(self.CreditLineEdit.text() or 0)
            existing_sub.scoreProcess = float(self.ProcessLineEdit.text() or 0)
            existing_sub.scoreMidterm = float(self.MidtermLineEdit.text() or 0)
            existing_sub.scoreFinal = float(self.FinalLineEdit.text() or 0)
        except ValueError:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Số liệu nhập vào không hợp lệ!")
            return

        # 3. Lưu file và cập nhật bảng
        self.sub_manager.export_json()
        self.display_subjects()
        QMessageBox.information(self.MainWindow, "Thông báo", f"Đã cập nhật thông tin môn {Subname}!")

    def process_delete_subject(self):
        Subname = self.NameLineEdit.text()
        if Subname == "":
            QMessageBox.critical(self.MainWindow, "Lỗi xóa", "Bạn phải chọn một môn học để xóa!")
            return
        dlg = QMessageBox.question(
            self.MainWindow,
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa môn [{Subname}] không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if dlg == QMessageBox.StandardButton.Yes:
            ret = self.sub_manager.delete_item(Subname)
            if ret:
                # Làm mới giao diện
                self.sub_manager.delete_item(Subname)
                self.display_subjects()
                QMessageBox.information(self.MainWindow, "Thông báo", "Đã xóa thành công!")
            else:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy môn học trong dữ liệu!")




    # ===================================================================
    # LOGIC RIÊNG CHO TAB 3: FINANCE MANAGEMENT
    # ===================================================================

    # Phần I: add expense và hiênr thị ở bảng expense list ở frame bên trái:
    def TAB3_PROCESS_ADD(self): #Xử lý khi bấm nút Add Expense
        ten=self.lineEditKhoanchi.text().strip()
        tien_str=self.lineEditGiatri.text().strip()
        loai=self.comboBoxLoaigia.currentText()
        ghi_chu=self.lineEditGhichu.text().strip()
        #Kiểm tra dữ liệucó hợp lệ ko
        if not ten or not tien_str:
            QMessageBox.warning(self.MainWindow,"Thiếu thông tin","Vui lòng nhập tên khoản chi và số tiền!")
            return
        try:
            tien=int(tien_str.replace(".", "").replace(",", ""))
            new_item=Expense(ten,tien,loai,ghi_chu)
            self.expense_manager.add_item(new_item)
            self.expense_manager.export_json("../datasets/expenses.json")
            # TRỪ TIỀN TRONG VÍ (liên quan phânf II)
            self.balance_manager.current_balance -= tien
            self.balance_manager.export_json("../datasets/balance.json")
            # Cập nhật lại bảng và xóa trắng ô nhập, cập nhật số dư ( PHẦN II):
            self.TAB3_UPDATE_TABLE_EXPENSE()
            self.TAB3_CLEAR_INPUTS()
            self.TAB3_UPDATE_BALANCE_UI()  #Cập nhật số dư mới bị trừ
            #Cập nhật lại tổng chi tiêu và so sánh với tháng trước
            self.TAB3_UPDATE_TOTAL_AND_COMPARE()
            self.TAB3_PROCESS_RIGHT_TABLE()  # Cập nhật bảng phải khi có dữ liệu mới
            QMessageBox.information(self.MainWindow, "Thành công", "Đã thêm khoản chi mới!")
        except ValueError:
            QMessageBox.warning(self.MainWindow,"Lỗi nhập liệu","Số tiền phải là con số!")
    def TAB3_UPDATE_TABLE_EXPENSE(self): #Hiển thị danh sách lên bảng tableExpenselist_3
        # logic: các khoản chi mới nhất sẽ hiển thị lên trên cùng.
        table=self.tableExpenselist_3
        table.setRowCount(0)
        data_list=self.expense_manager.items
        for row_index, item in enumerate(reversed(data_list)):
            table.insertRow(row_index)
            #Cột 0:Ngày
            table.setItem(row_index,0,QTableWidgetItem(str(item.ngay)))
            #Cột 1:Tên khoản chi
            table.setItem(row_index,1,QTableWidgetItem(str(item.khoan_chi)))
            #Cột 2:Số tiền(có dấu phẩy ngăn cách)
            money_str="{:,}".format(item.so_tien)
            table.setItem(row_index,2,QTableWidgetItem(money_str))
            #Cột 3:Danh mục
            table.setItem(row_index,3,QTableWidgetItem(str(item.danh_muc)))
            #Cột 4:Ghi chú
            table.setItem(row_index,4,QTableWidgetItem(str(item.ghi_chu)))
    def TAB3_CLEAR_INPUTS(self): #Xóa trắng các ô nhập liệu
        self.lineEditKhoanchi.clear()
        self.lineEditGiatri.clear()
        self.lineEditGhichu.clear()
        self.lineEditKhoanchi.setFocus()  #Đưa con trỏ chuột quay lại ô đầu tiên


    # Phần 2: Phần hiển thị số dư, thêm thu nhập mới, trừ đi khoản chi.
    def TAB3_UPDATE_BALANCE_UI(self): #Hàm cập nhật hiển thị số dư lên label_soduhientai
        money_str="{:,.0f} đ".format(self.balance_manager.current_balance)
        self.label_soduhientai.setText(money_str)
    def TAB3_PROCESS_ADD_INCOME(self): #Xử lý khi bấm nút Add Income (Thêm thu nhập)
        tien_nhap=self.lineEditIncome.text().strip()
        if not tien_nhap:
            return
        try:
            tien=int(tien_nhap.replace(".", "").replace(",", ""))
            self.balance_manager.current_balance+=tien
            self.balance_manager.export_json("../datasets/balance.json")
            #Cập nhật lại giao diện
            self.TAB3_UPDATE_BALANCE_UI()
            self.lineEditIncome.clear()
            QMessageBox.information(self.MainWindow, "Ting Ting!", f"Đã nạp thêm {tien:,} đ vào tài khoản.")
        except ValueError:
            QMessageBox.warning(self.MainWindow,"Lỗi","Vui lòng nhập số tiền hợp lệ!")


    # PHẦN III: XỬ LÍ HIỂN THỊ VÀ SO SÁNH TỔNG CHI TIÊU SO VỚI THÁNG TRƯỚC.
    def TAB3_UPDATE_TOTAL_AND_COMPARE(self): #Tính tổng chi tiêu tháng này và so sánh với tháng trước
        # Xác định thời gian hiện tại
        today=datetime.datetime.now()
        current_month=today.month
        current_year= today.year
        # Xác định tháng trước
        if current_month== 1:
            prev_month= 12
            prev_year= current_year- 1
        else:
            prev_month=current_month-1
            prev_year= current_year
        #Tính toán từ danh sách expenses
        total_current_month= 0
        total_prev_month= 0
        for item in self.expense_manager.items:
            try:
                #Chuyển chuỗi thành ngày tháng
                date_obj= datetime.datetime.strptime(item.ngay,"%d/%m/%Y")
                if date_obj.month == current_month and date_obj.year == current_year:
                    total_current_month += item.so_tien
                #+ tháng trước nếu ko khớp
                elif date_obj.month == prev_month and date_obj.year == prev_year:
                    total_prev_month += item.so_tien
            except ValueError:
                continue  #Bỏ qua nếu lỗi ngày tháng
        #Hiển thị Tổng chi tiêu tháng này lên label_total_3
        self.label_total_3.setText(f"{total_current_month:,.0f} đ")
        # Xử lý logic So sánh Tăng/Giảm
        diff=total_current_month-total_prev_month
        if diff>0:#Chi nhiều hơn tháng trước-> Màu Đỏ(Cảnh báo)
            self.label_tanggiam.setText(f"Tăng {diff:,.0f} đ so với tháng trước")
            self.label_tanggiam.setStyleSheet("color: red;font-weight:bold;")
        elif diff<0:#Chi ít hơn tháng trước-> Màu Xanh(Tốt)
            self.label_tanggiam.setText(f"Giảm {abs(diff):,.0f} đ so với tháng trước")
            self.label_tanggiam.setStyleSheet("color:green;font-weight: bold;")
        else: # Bằng nhau hoặc tháng đầu tiên( lấy tháng 1 làm gốc) (diff = 0)
            self.label_tanggiam.setText("Chưa có biến động so với tháng trước")
            self.label_tanggiam.setStyleSheet("color: black;")


    # PHẦN IV: XỬ LÝ BẢNG BÊN PHẢI (TÌM KIẾM - SẮP XẾP - LỌC)
    def TAB3_PROCESS_RIGHT_TABLE(self):#Hàm xử lý logic tổng hợp cho bảng bên phải
        current_list = self.expense_manager.items.copy()
        #XỬ LÝ TÌM KIẾM THEO NGÀY
        keyword = self.lineEdittimkhoanchi_3.text().strip()
        if keyword:
            current_list = [item for item in current_list if keyword in item.ngay]
        #XỬ LÝ LỌC DANH MỤC
        category = self.comboBoxloc_2.currentText()
        # Chỉ lọc nếu người dùng chọn một danh mục cụ thể(khác rỗng)
        if category and category.strip() != "":
            current_list = [item for item in current_list if item.danh_muc == category]
        # XỬ LÝ SẮP XẾP
        sort_mode=self.comboBoxsapxep_2.currentText()
        if sort_mode=="Tăng dần":
            current_list.sort(key=lambda x: x.so_tien, reverse=False)
        elif sort_mode=="Giảm dần":
            current_list.sort(key=lambda x: x.so_tien, reverse=True)
        else:
            current_list.reverse()
        #HIỂN THỊ RA BẢNG
        self.TAB3_DRAW_RIGHT_TABLE(current_list)
    def TAB3_DRAW_RIGHT_TABLE(self, data_list):
        table=self.tablelExpenseist2_3
        table.setRowCount(0)
        for row_index, item in enumerate(data_list):
            table.insertRow(row_index)
            table.setItem(row_index,0,QTableWidgetItem(str(item.ngay)))
            table.setItem(row_index,1,QTableWidgetItem(str(item.khoan_chi)))
            table.setItem(row_index,2,QTableWidgetItem("{:,}".format(item.so_tien)))
            table.setItem(row_index,3,QTableWidgetItem(str(item.danh_muc)))
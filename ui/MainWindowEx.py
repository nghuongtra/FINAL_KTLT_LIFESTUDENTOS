from functools import partial
import random
import os
import pandas as pd
import json
import datetime

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox,QPushButton,QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog



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

#import của tab insights
import io
# import matplotlib.pyplot as plt
from PyQt6.QtGui import QImage, QPixmap


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
#----- TAB 5------------------------------------------


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
        self.pushButtonInsights.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageInsight))
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

        # OVERSIGHT & INSIGHTS
        self.pushButtonInsights.clicked.connect(self.updateinsight)
        self.xuatfileexcel.clicked.connect(self.process_excel_csv)
        if hasattr(self, 'lineEditInputGPA'):
            self.lineEditInputGPA.setReadOnly(True)
            self.lineEditInputGPA.setPlaceholderText("Đang tính...")
        if hasattr(self, 'lineEditInputTienDo'):
            self.lineEditInputTienDo.setPlaceholderText("Đang tính...")
            self.lineEditInputTienDo.setReadOnly(True)
        if hasattr(self, 'lineEditInputTienDo_2'):
            self.lineEditInputTienDo_2.setPlaceholderText("Đang tính...")
            self.lineEditInputTienDo_2.setReadOnly(True)

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


#=================================OVERSIGHT&INSIGHTS=======================================
    # {Mở phần insight
    ############################ XỬ LÍ LOGIC GPA ############################################
    def kiem_tra_trang_hien_tai(self, index):
        if self.stackedWidget.widget(index) == self.pageInsight:
            try:
                self.update_tiendo_hoctap()
                self.updateinsight()
            except Exception as e:
                print(f"LỖI KHI CHUYỂN TAB INSIGHT: {e}")
                import traceback
                traceback.print_exc()

    def update_tiendo_hoctap(self):
        try:
            if not hasattr(self, 'sub_manager'): return

            danh_sach_mon = self.sub_manager.list
            tong_tin_chi_da_hoc = 0
            for mon_hoc in danh_sach_mon:
                try:
                    tong_tin_chi_da_hoc += float(mon_hoc.credit)
                except:
                    continue
            Tong_tin_chi = 130
            phan_tram = 0
            if Tong_tin_chi > 0:
                phan_tram = (tong_tin_chi_da_hoc / Tong_tin_chi) * 100

            # Kiểm tra tồn tại widget trước khi gán
            if hasattr(self, 'lineEdit_TienDo'):
                self.lineEdit_TienDo.setText(f"{phan_tram:.2f}%")
        except Exception as e:
            print(f"Lỗi update_tiendo_hoctap: {e}")

    def lay_tong_chi_tieu_thang(self, thang, nam):
        tong = 0
        if not hasattr(self, 'expense_manager'):
            return 0

        for item in self.expense_manager.items:
            try:
                date_obj = datetime.datetime.strptime(item.ngay, "%d/%m/%Y")
                if date_obj.month == thang and date_obj.year == nam:
                    tong += item.so_tien
            except:
                continue
        return tong

    def lay_gpa_ky_truoc(self):
        try:
            path = "../datasets/gpa_user.json"
            if not os.path.exists(path): return 0.0

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return float(data.get("gpa_ky_truoc", 0.0))
        except:
            return 0.0

    def ve_bieu_do_trend(self, gpa_cu, gpa_hien_tai):
            fig, ax = plt.subplots(figsize=(4, 1.5), dpi=100)
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')
            x = ["Kỳ trước", "Kỳ này"]
            y = [gpa_cu, gpa_hien_tai]
            color = '#27ae60' if gpa_hien_tai >= gpa_cu else '#c0392b'
            ax.plot(x, y, marker='o', color=color, linewidth=2.5, markersize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.get_yaxis().set_visible(False)
            for i, v in enumerate(y):
                ax.text(i, v + 0.1, f"{v:.2f}", ha='center', color=color, fontweight='bold')
            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True)
            plt.close(fig)
            buf.seek(0)
            qimg = QImage.fromData(buf.getvalue())
            return QPixmap.fromImage(qimg)

    def updateinsight(self):
        try:
            # =========================================================================
            # PHẦN 1: TÍNH TOÁN GPA & TIẾN ĐỘ
            # =========================================================================
            tong_tin_chi_tich_luy = 0
            tong_diem_tich_luy = 0.0

            # 1.1 Quét danh sách môn học
            if hasattr(self, 'sub_manager') and hasattr(self.sub_manager, 'list'):
                for mon in self.sub_manager.list:
                    try:
                        tin_chi = float(mon.credit)
                        diem_so = float(mon.scoreFinal)

                        tong_tin_chi_tich_luy += tin_chi
                        tong_diem_tich_luy += (diem_so * tin_chi)
                    except (ValueError, AttributeError):
                        continue

            GPA = 0.0
            if tong_tin_chi_tich_luy > 0:
                GPA = tong_diem_tich_luy / tong_tin_chi_tich_luy

            # Hiển thị GPA
            if hasattr(self, 'lineEditInputGPA'):
                self.lineEditInputGPA.setText(f"{GPA:.2f}")
                self.lineEditInputGPA.setReadOnly(True)
            if hasattr(self, 'insight_GPA_3'):
                self.insight_GPA_3.setText(f"{GPA:.2f}")

            # 1.3 Tính & Hiển thị Tiến Độ
            TONG_TIN_CHI_RA_TRUONG = 130
            phan_tram_tiendo = 0.0

            if tong_tin_chi_tich_luy > 0:
                phan_tram_tiendo = (tong_tin_chi_tich_luy / TONG_TIN_CHI_RA_TRUONG) * 100

            if phan_tram_tiendo > 100: phan_tram_tiendo = 100

            text_tiendo = f"{phan_tram_tiendo:.2f}%"

            if hasattr(self, 'lineEditInputTienDo'):
                self.lineEditInputTienDo.setText(text_tiendo)
                self.lineEditInputTienDo.setReadOnly(True)

            # 1.4 So sánh GPA cũ
            gpa_cu = self.lay_gpa_ky_truoc()
            chenh_lech = GPA - gpa_cu

            if hasattr(self, 'number1_4') and hasattr(self, 'insight_GPA_3'):
                if chenh_lech >= 0:
                    text = f"↑ Tăng {chenh_lech:.2f} so với kỳ trước"
                    color = "green"
                else:
                    text = f"↓ Giảm {abs(chenh_lech):.2f} so với kỳ trước"
                    color = "red"

                self.number1_4.setText(text)
                self.number1_4.setStyleSheet(f"color: {color}; font-weight: bold;")
            if hasattr(self, 'label_linechart'):
                pixmap_chart = self.ve_bieu_do_trend(gpa_cu, GPA)
                self.label_linechart.setPixmap(pixmap_chart)
                self.label_linechart.setScaledContents(True)
                self.label_linechart.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # ========================================================================================
            # 2. XỬ LÝ TÀI CHÍNH
# ==========================================================================================
            so_du = 0.0
            if hasattr(self, 'balance_manager'):
                so_du = self.balance_manager.current_balance

            if hasattr(self, 'lineEditInputTienDo_2'):
                self.lineEditInputTienDo_2.setText(f"{so_du:,.0f} VNĐ")
                self.lineEditInputTienDo_2.setReadOnly(True)

# ==============================TOP SPENDING ====================================
            danh_sach_chi_tieu = {}
            tong_tien_chi_tieu = 0.0
            if hasattr(self, 'expense_manager') and hasattr(self.expense_manager, 'items'):
                for item in self.expense_manager.items:
                    try:
                        muc_dich = item.danh_muc.lower() if item.danh_muc else "khác"
                        # Xử lý số tiền
                        tien_str = str(item.so_tien).replace(',', '').replace('.', '')
                        try:
                            tien = float(item.so_tien)
                        except:
                            if tien_str.isdigit():
                                tien = float(tien_str)
                            else:
                                continue

                        if muc_dich in danh_sach_chi_tieu:
                            danh_sach_chi_tieu[muc_dich] += tien
                        else:
                            danh_sach_chi_tieu[muc_dich] = tien

                        tong_tien_chi_tieu += tien
                    except:
                        continue

# =======================HIỂN THỊ ICON TOP SPENDING ====================================
            if danh_sach_chi_tieu:
                top_cat = max(danh_sach_chi_tieu, key=danh_sach_chi_tieu.get)
                top_val = danh_sach_chi_tieu[top_cat]
                # Tính phần trăm
                percent = (top_val / tong_tien_chi_tieu) * 100 if tong_tien_chi_tieu > 0 else 0
                if hasattr(self, 'number2_6'):
                    self.number2_6.setText(f"{percent:.1f}%")

                top_cat = top_cat.lower()
                icon_map = {
                    "mua sắm": "../images/mua_sam.png",
                    "ăn uống": "../images/food.png",
                    "học tập": "../images/study.png",
                    "đi lại": "../images/xe_co.png",
                    "giải trí": "../images/tro_choi.png",
                    "sức khỏe":"../images/y_te.png"
                }

                icon = icon_map.get(top_cat)

                self.topspending.setPixmap(QPixmap(icon))
                self.topspending.setScaledContents(True)

#  ===================  PHẦN TIPS & LỜI KHUYÊN ============================================
            # Tính toán xem có bị lố tay không????
            today = datetime.datetime.now()
            chitieu_thang_nay = tong_tien_chi_tieu

            # Logic: Tiêu quá 2 trăm/tháng là cảnh báo
            bi_lo_tay = False
            if chitieu_thang_nay > 200000:
                bi_lo_tay = True

            tip_tietkiem = ["Tách riêng 2 ví: 1 Tiêu dùng - 1 Tiết kiệm. Đừng để chung!",
                        "Chia nhỏ ngân sách: Đặt hạn mức theo Tuần thay vì Tháng.",
                        "Quy tắc 24h: Tự hỏi bản thân cần hay muốn? và chờ 1-2 ngày trước khi mua.",
                        " Ưu tiên cơm nhà: Vừa an toàn, sạch sẽ lại vừa tiết kiệm.",
                        "Ghi chép chi vặt: Trà sữa, ship đồ ăn chính là thủ phạm gây cháy túi!",
                            "Đừng quên quyền năng thẻ Sinh Viên: Giảm giá khắp mọi nơi!",
                            "Quẹt thẻ thì sướng, trả tiền mặt mới thấy xót. Hãy dùng tiền mặt!"]

            tip_caithien = [
            "Hổng kiến thức khiến GPA thấp. Hãy ôn lại cơ bản ngay!",
            "Thử Pomodoro: 25 phút Học - 5 phút Nghỉ.",
            "Đừng ngại hỏi giảng viên hoặc bạn bè khi chưa hiểu bài.",
            "Tập trung tuyệt đối: Tắt thông báo điện thoại khi đang học.",
            "Ghi chép thông minh: Sử dụng sơ đồ tư duy (Mindmap) để hệ thống bài học.",
            "Đừng học vẹt! Hãy hiểu rõ bản chất vấn đề!!",
            "Review lại bài ngay sau khi học xong giúp nhớ lâu gấp 3 lần!!",
            "Phương pháp Feynman: Thử giảng lại kiến thức cho người khác để hiểu sâu hơn!"
        ]
            tip_hoctot = ["Phong độ rất tốt! Hãy duy trì thói quen hiện tại.",
                      "Đừng quên cân bằng giữa học và chơi để tránh Burn-out.",
                      "Bạn có thể bắt đầu tìm kiếm học bổng hoặc tham gia nghiên cứu.",
                      "Hãy thử thách bản thân với các môn học khó hơn.",
                      "Chia sẻ kiến thức với bạn bè cũng là cách để ôn bài hiệu quả.",
                      "Chuẩn bị sớm cho các chứng chỉ ngoại ngữ hoặc kỹ năng mềm.",
                      "Giữ sức khỏe! Ngủ đủ giấc giúp não bộ hoạt động tối ưu."
                      ]

            nhanxet = ""
            tips = ""
            ghichu = ""

            # Logic chọn lời khuyên
            if GPA >= 8.0 and bi_lo_tay is False:
                nhanxet = "Xuất sắc! Học giỏi - Tài chính vững!"
                if hasattr(self, 'advice_2'): self.advice_2.setStyleSheet(
                    "background-color:#63A693; color:black; font-weight:bold;")
                tips = random.choice(tip_hoctot)
                ghichu = "NOTE: AN TOÀN"
                if hasattr(self, 'shortcomment_2'): self.shortcomment_2.setStyleSheet(
                    "background-color:#63A693; color:white; font-weight:bold;")

            elif GPA >= 8.0 and bi_lo_tay is True:
                nhanxet = "Học tốt! Nhưng xài tiền hơi lố."
                if hasattr(self, 'advice_2'): self.advice_2.setStyleSheet(
                    "background-color:#FDFD96; color:black; font-weight:bold;")
                tips = random.choice(tip_tietkiem)
                ghichu = "NOTE: CẢNH BÁO"
                if hasattr(self, 'shortcomment_2'): self.shortcomment_2.setStyleSheet(
                    "background-color:#FFCAA1; color:black; font-weight:bold;")

            elif GPA < 8.0 and bi_lo_tay is False:
                if GPA >= 6.5:
                    nhanxet = "Học lực Khá! Tài chính ổn."
                else:
                    nhanxet = "Cảnh báo học tập!"
                if hasattr(self, 'advice_2'): self.advice_2.setStyleSheet(
                    "background-color:#FDFD96; color:black; font-weight:bold;")
                tips = random.choice(tip_caithien)
                ghichu = "NOTE: CẢNH BÁO"
                if hasattr(self, 'shortcomment_2'): self.shortcomment_2.setStyleSheet(
                    "background-color:#FFCAA1; color:black; font-weight:bold;")

            elif GPA < 8.0 and bi_lo_tay is True:
                nhanxet = "BÁO ĐỘNG ĐỎ: Tiền và Điểm đều nguy cấp!"
                if hasattr(self, 'advice_2'): self.advice_2.setStyleSheet(
                    "background-color:#FF6961; color:white; font-weight:bold;")
                tips = random.choice(tip_tietkiem)
                ghichu = "NOTE: BÁO ĐỘNG ĐỎ"
                if hasattr(self, 'shortcomment_2'): self.shortcomment_2.setStyleSheet(
                    "background-color:#FF6961; color:white; font-weight:bold;")

            # In kết quả
            if hasattr(self, 'advice_2'): self.advice_2.setText(nhanxet)
            if hasattr(self, 'input_tips'): self.input_tips.setText(tips)
            if hasattr(self, 'shortcomment_2'): self.shortcomment_2.setText(ghichu)

        except Exception as e:
            print(f"LỖI NGHIÊM TRỌNG TRONG UPDATE INSIGHT: {e}")
            import traceback
            traceback.print_exc()

        ####################### XỬ LÍ XUẤT FILE EXCEL/CSV##############################

    def process_excel_csv(self):
        try:
            msgBox = QMessageBox(self.MainWindow)
            msgBox.setIcon(QMessageBox.Icon.Question)
            msgBox.setWindowTitle("Xuất danh sách")
            msgBox.setText("Bạn muốn xuất file theo định dạng nào?")

            btn_excel = msgBox.addButton("EXCEL", QMessageBox.ButtonRole.ActionRole)
            btn_csv = msgBox.addButton("CSV", QMessageBox.ButtonRole.ActionRole)
            btn_cancel = msgBox.addButton("Hủy", QMessageBox.ButtonRole.RejectRole)

            msgBox.exec()

            clicked_button = msgBox.clickedButton()

            # Kiểm tra click
            if clicked_button == btn_excel:
                self.export_to_excel()
            elif clicked_button == btn_csv:
                self.export_to_csv()

        except Exception as e:
            print(f"Lỗi tại process_excel_csv: {e}")

    def lay_du_lieu_oversight(self):
        try:
            val_gpa = self.lineEditInputGPA.text() if hasattr(self, 'lineEditInputGPA') else ""
            val_tiendo = self.lineEditInputTienDo.text() if hasattr(self, 'lineEditInputTienDo') else ""
            val_vitien = self.lineEditInputTienDo_2.text() if hasattr(self, 'lineEditInputTienDo_2') else ""
            val_nhanxet = self.advice_2.text() if hasattr(self, 'advice_2') else ""
            val_tips = self.input_tips.text() if hasattr(self, 'input_tips') else ""

            data = {
                "HẠNG MỤC": ["GPA Hiện tại", "Tiến độ học tập", "Số dư tài chính", "Đánh giá tổng quan",
                             "Lời khuyên chi tiết"],
                "KẾT QUẢ": [val_gpa, val_tiendo, val_vitien, val_nhanxet, val_tips]
            }
            return pd.DataFrame(data)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi Dữ Liệu", f"Không thể lấy dữ liệu: {e}")
            return None

    def export_to_excel(self):
        try:
            df = self.lay_du_lieu_oversight()
            if df is None: return

            # Tạo tên file
            thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ten_mac_dinh = f"BaoCao_Oversight_{thoi_gian}.xlsx"
            duong_dan, _ = QFileDialog.getSaveFileName(
                self.MainWindow,
                "Lưu file Excel",
                ten_mac_dinh,
                "Excel Files (*.xlsx)"
            )

            if duong_dan:
                df.to_excel(duong_dan, index=False, engine='openpyxl')
                QMessageBox.information(self.MainWindow, "Thành công", f"Đã xuất file tại:\n{duong_dan}")

        except ImportError:
            QMessageBox.warning(self.MainWindow, "Thiếu thư viện", "Vui lòng cài đặt thư viện: pip install openpyxl")
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Lỗi", f"Không thể xuất file Excel:\n{e}")

    def export_to_csv(self):
        try:
            df = self.lay_du_lieu_oversight()
            if df is None: return

            thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ten_mac_dinh = f"BaoCao_Oversight_{thoi_gian}.csv"
            duong_dan, _ = QFileDialog.getSaveFileName(
                self.MainWindow,
                "Lưu file CSV",
                ten_mac_dinh,
                "CSV Files (*.csv)"
            )

            if duong_dan:
                # utf-8-sig giúp mở trong Excel không bị lỗi font tiếng Việt
                df.to_csv(duong_dan, index=False, encoding='utf-8-sig')
                QMessageBox.information(self.MainWindow, "Thành công", f"Đã xuất file tại:\n{duong_dan}")

        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Lỗi", f"Không thể xuất file CSV:\n{e}")
# Đóng phần insights }

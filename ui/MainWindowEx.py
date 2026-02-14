
import datetime
import random
import os
import pandas as pd

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox, QFileDialog

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
        #Phần của tab finance management
        self.pushButtonNew.clicked.connect(self.processNew)
        self.pushButtonSave.clicked.connect(self.processSave)
        self.pushButtonDeleteTask.clicked.connect(self.processRemove)
        self.listWidgetTask.itemSelectionChanged.connect(self.processItemSelection)
        self.dateEditDeadline.dateChanged.connect(self.updateCountdown)
        self.timeEditDeadline.timeChanged.connect(self.updateCountdown)
        #Phần của tab insights
        self.stackedWidget.currentChanged.connect(self.kiem_tra_trang_hien_tai)
        self.xuatfileexcel.clicked.connect(self.process_excel_csv)


        #TAB 3: FINANCE MANAGEMENT.
        self.pushButtonAddExpense.clicked.connect(self.TAB3_PROCESS_ADD) #PHẦN I
        self.pushButton_addincome.clicked.connect(self.TAB3_PROCESS_ADD_INCOME) #PHẦN II
        self.pushButtonsearch_3.clicked.connect(self.TAB3_PROCESS_RIGHT_TABLE)
        self.comboBoxsapxep_2.currentIndexChanged.connect(self.TAB3_PROCESS_RIGHT_TABLE)
        self.comboBoxloc_2.currentIndexChanged.connect(self.TAB3_PROCESS_RIGHT_TABLE)

    def process_viewdetail(self):
        gpa_text = self.lineEditGPA.text()
        if gpa_text:
            gpa_float = float(gpa_text)
            self.labelGPA.setText(f"{gpa_float}")
            n = (gpa_float / 4) * 10
            self.labelGrade.setText(f"{n:.2f}")

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
#{ Phần của tab finance management
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
#} đóng phần tab finance management


#{Mở phần ínsight
    def kiem_tra_trang_hien_tai(self,index):
        if index == 4:
            self.updateinsight()

    def update_tiendo_hoctap(self):
        danh_sach_mon = self.adm_subject.list
        tong_tin_chi_da_hoc = 0
        for mon_hoc in danh_sach_mon:
            try:
                tong_tin_chi_da_hoc += mon_hoc.credit
            except:
                continue
        Tong_tin_chi = 130
        phan_tram = 0
        if Tong_tin_chi > 0:
            phan_tram = (tong_tin_chi_da_hoc / Tong_tin_chi) * 100
        self.lineEdit_TienDo.setText(f"{phan_tram:.2f}%")

    def updateinsight(self):
        text_GPA=self.lineEditGPA.text()
        if text_GPA == '':
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu GPA!\nVui lòng thử lại.")
            self.stackWidget.setCurrentIndex(1)
            return
        else:
            GPA=float(text_GPA)

        text_money=self.current_balance.text()
        if text_money == '':
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu!\nVui lòng thử lại.")
            self.stackWidget.setCurrentIndex(2)
            return
        else:
            money=float(text_money)
        text_money = self.current_balance.text()
        clean_money = text_money.replace('.', '').replace(',', '').replace('VNĐ', '').replace('đ', '').strip()
        money = float(clean_money) if clean_money else 0.0

        # Lấy Chi tiêu Tháng này
        text_chitieu = self.label_10.text()
        clean_chitieu = text_chitieu.replace('.', '').replace(',', '').replace('VNĐ', '').replace('đ', '').strip()
        chitieu_thang_nay = float(clean_chitieu) if clean_chitieu else 0.0

        # --- TÍNH CHI TIÊU THÁNG TRƯỚC
        adm_expense = Expenses()
        adm_expense.load_json("datasets/expenses.json")
        today = datetime.now()
        # 2. Xác định tháng trước
        if today.month == 1:
            last_month = 12
            last_year = today.year - 1
        else:
            last_month = today.month - 1
            last_year = today.year

        # 3.tính tổng tiền
        chitieu_thang_truoc = 0
        for item in adm_expense.items:
            try:
                # Giả sử ngày lưu dạng "dd/mm/yyyy"
                # Nếu file json lưu dạng "yyyy-mm-dd" thì sửa lại format nhé
                date_obj = datetime.strptime(item.ngay, "%d/%m/%Y")

                if date_obj.month == last_month and date_obj.year == last_year:
                    chitieu_thang_truoc += float(item.so_tien)
            except:
                continue  # Bỏ qua nếu lỗi định dạng ngày/tiền

        # --- 3. LOGIC SO SÁNH "LỐ TAY" ---
        bi_lo_tay = False
        # Nếu chưa có dữ liệu tháng này (chitieu_thang_nay = 0) thì không tính là lố
        if chitieu_thang_nay > 0:
            chenh_lech = chitieu_thang_nay - chitieu_thang_truoc
            # Lớn hơn 100k mới báo
            if chenh_lech > 100000:
                bi_lo_tay = True

        #Nhận xét
        ghichu=""
        nhanxet=""
        tips=""
        tip_tietkiem=["Dùng 1 tài khoản để tiêu – 1 tài khoản để tiết kiệm, đừng để chung.",
                      "Bạn hãy thử đặt hạn mức chi tiêu theo tuần thay vì hạn mức chi tiêu theo tháng để dễ kiểm soát hơn nhé!"
                      "Hãy luôn đặt câu hỏi Thực sự mình có cần món đồ đó không? trước khi mua. Cho bản thân từ 24-48h để suy nghĩ về món đồ đó bạn nhé!"
                      " Ưu tiên nấu ăn tại gia, vừa an toàn mà còn tiết kiệm bạn nhé!"
                      "Ghi lại mọi khoản chi nhỏ, vì chính trà sữa, ship đồ ăn mới là “thủ phạm” hao tiền nhất đấy!!!!"]

        tip_caithien=[
            "GPA không như mong muốn thường do chưa hiểu bản chất và có lỗ hổng kiến thức. Hãy xem lại kiến thức cơ bản và củng cố nhé.",
            "Thử phương pháp Pomodoro: Học 25p - Nghỉ 5p để tránh mệt mỏi.",
            "Đừng ngại hỏi giảng viên hoặc bạn bè khi chưa hiểu bài.",
            "Tắt thông báo điện thoại khi học. Sự tập trung là chìa khóa!",
            "Hãy ghi chú lại bài giảng bằng sơ đồ tư duy Mindmap.",
            "Đừng học vẹt! Hãy cố gắng hiểu bản chất vấn đề bạn nheee!!!",
            "Review lại bài ngay sau khi học xong giúp nhớ lâu gấp 3 lần!!"
            "Hãy thử phương pháp Feynman!! Đừng chỉ hiểu trong đầu. Hãy thử nói ra giống như giảng bài cho 1 ai đó để bạn nắm kiến thức vững hơn nhé!!"
        ]
        tip_hoctot=["Phong độ rất tốt! Hãy duy trì thói quen hiện tại.",
            "Đừng quên cân bằng giữa học và chơi để tránh Burn-out.",
            "Bạn có thể bắt đầu tìm kiếm học bổng hoặc tham gia nghiên cứu.",
            "Hãy thử thách bản thân với các môn học khó hơn.",
            "Chia sẻ kiến thức với bạn bè cũng là cách để ôn bài hiệu quả.",
            "Chuẩn bị sớm cho các chứng chỉ ngoại ngữ hoặc kỹ năng mềm.",
            "Giữ sức khỏe! Ngủ đủ giấc giúp não bộ hoạt động tối ưu."
        ]
            # 1. HỌC GIỎI +NHIỀU TIỀN
        if GPA >= 3.2 and bi_lo_tay is True:
            nhanxet = "Xuất sắc! Con nhà người ta đây rồi: Học giỏi - Tài chính vững!"
            tips=random.choice(tip_hoctot)
            ghichu = "NOTE:AN TOÀN"
            self.shortcomment_2.setStyleSheet("background-color:green; color:white; font-weight:bold;")

            # 2. HỌC GIỎI (>=3.2) + HẾT TIỀN
        elif GPA >= 3.2 and bi_lo_tay is False:
            nhanxet = "Học tốt nha! Mà xài tiền hơi lố rồi đó, coi chừng cuối tháng ăn mì gói."
            self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
            tips =random.choice(tip_tietkiem)+random.choice(tip_hoctot)
            ghichu="NOTE: CẢNH BÁO"
            self.shortcomment_2.setStyleSheet("background-color: orange; color:black; font-weight:bold;")

            # 3. HỌC KHÁ/TRUNG BÌNH (<3.2) + TIỀN NHIỀU
        elif GPA < 3.2 and bi_lo_tay is True:
            nhanxet = "Tài chính rủng rỉnh nhưng việc học cần tập trung hơn nhé!"
            self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
            ghichu = "NOTE: CẢNH BÁO"
            self.shortcomment_2.setStyleSheet("background-color: orange; color:black; font-weight:bold;")
            if GPA >= 2.5:
                nhanxet = "Học lực Khá! Bạn thử đổi phương pháp học xem sao!!"
                self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
                ghichu = "NOTE: CẢNH BÁO"
                self.shortcomment_2.setStyleSheet("background-color: orange; color:black; font-weight:bold;")
            else:
                nhanxet = "Cảnh báo học tập! Đừng để tiền làm mờ mắt kiến thức."
                self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
                ghichu = "NOTE: CẢNH BÁO"
                self.shortcomment_2.setStyleSheet("background-color: orange; color:black; font-weight:bold;")

            tips = random.choice(tip_caithien)

            # 4. HỌC KÉM + HẾT TIỀN
        else:
            nhanxet = "BÁO ĐỘNG ĐỎ: Cả Tiền và Điểm đều nguy cấp! Cần chấn chỉnh gấp!"
            self.advice_2.setStyleSheet("background-color: red; color:white; font-weight:bold;")
            tips = random.choice(tip_tietkiem)+random.choice(tip_caithien)
            ghichu = "NOTE: BÁO ĐỘNG ĐỎ"
            self.shortcomment_2.setStyleSheet("background-color:red; color:white; font-weight:bold;")
        self.advice_2.setText(nhanxet)
        self.input_tips.setText(tips)
        self.shortcomment_2.setText(ghichu)

        ##### GPA TREND ########
        self.insight_GPA.setText(str(GPA))
        # Giả sử GPA kì trước là 3.0
        gpa_ky_truoc = 3.0
        chenh_lech = GPA - gpa_ky_truoc
        if chenh_lech > 0:
            self.number1_2.setText(f"+{chenh_lech:.1f}")
            self.number1_2.setStyleSheet("color: green; font-weight: bold;")
        elif chenh_lech < 0:
            self.number1_2.setText(f"-{chenh_lech:.1f}")
            self.number1_2.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.number1_2.setText("0.0")

         ###### TOP SPENDING #######
        danh_sach_chi_tieu = {
            "mua sắm": 2500000,
            "ăn uống": 1500000,
            "học tập": 500000,
            "đi lại": 100000,
            "chi tiêu cho mục đích khác":300000
        }
        if danh_sach_chi_tieu:
            # Tìm cái tiêu nhiều nhất
            top_cat = max(danh_sach_chi_tieu, key=danh_sach_chi_tieu.get)
            top_val = danh_sach_chi_tieu[top_cat]
            total_spend = sum(danh_sach_chi_tieu.values())
            if total_spend >0:
                percent = (top_val / total_spend) * 100
            else:
                percent = 0
            self.number2_2.setText(f"{percent:.1f}%")
            icon = ""
            if top_cat == "mua sắm":
                icon = "../images/pic_shopping.png"
            elif top_cat == "ăn uống":
                icon = "../images/pic_food.png"
            elif top_cat == "học tập":
                icon= "../images/pic_books.png"
            elif top_cat == "đi lại":
                icon = "../images/pic_car.png"
            elif top_cat == "chi tiêu cho mục đích khác":
                icon = "../images/pic_other.png"

            if icon:
                self.topspending.setPixmap(QPixmap(icon))
                self.topspending.setScaledContents(True)

    def process_excel_csv(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setWindowTitle("Xuất danh sách")
        msgBox.setText("Bạn muốn xuất file theo định dạng nào?")

        btn_excel = msgBox.addButton("EXCEL", QMessageBox.ButtonRole.ActionRole)
        btn_csv = msgBox.addButton("CSV", QMessageBox.ButtonRole.ActionRole)
        btn_cancel = msgBox.addButton("Hủy", QMessageBox.ButtonRole.RejectRole)
        msgBox.exec()
        if msgBox.clickedButton() == btn_excel:
            self.export_to_excel()
        elif msgBox.clickedButton() == btn_csv:
            self.export_to_csv()
        elif msgBox.clickedButton() == btn_cancel:
            return

    def lay_du_lieu_oversight(self):
        val_gpa=self.lineEditInputGPA.text()
        val_tiendo=self.lineEditInputTiendo.text()
        val_vitien=self.lineEditInputVitien.text()
        val_nhanxet=self.lineEditInputNhanxet.text()
        val_tips=self.lineEditInputTips.text()
        data = {
            "HẠNG MỤC": [
                "GPA Hiện tại",
                "Tiến độ học tập",
                "Số dư tài chính",
                "Đánh giá tổng quan",
                "Lời khuyên chi tiết"
            ],
            "KẾT QUẢ": [
                val_gpa,
                val_tiendo,
                val_vitien,
                val_nhanxet,
                val_tips
            ]
        }
        df = pd.DataFrame(data)
        return df

    def export_to_excel(self):
        df = self.lay_du_lieu_oversight()
        if df is None: return
        #Tạo tên file mặc định
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        ten_mac_dinh = f"BaoCao_Oversight_{thoi_gian}.xlsx"
        #Mở cửa sổ chọn nơi lưu
        duong_dan, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu file Excel",
            ten_mac_dinh,
            "Excel Files (*.xlsx)"
        )
        #Lưu file
        if duong_dan:
            df.to_excel(duong_dan, index=False)
            QMessageBox.information(self, "Thành công", f"Đã xuất file tại:\n{duong_dan}")

    def export_to_csv(self):
        df = self.lay_du_lieu_oversight()
        if df is None: return
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        ten_mac_dinh = f"BaoCao_Oversight_{thoi_gian}.csv"
        duong_dan, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu file CSV",
            ten_mac_dinh,
            "CSV Files (*.csv)"
        )
        if duong_dan:
            df.to_csv(duong_dan, index=False, encoding='utf-8-sig')
            QMessageBox.information(self, "Thành công", f"Đã xuất file tại:\n{duong_dan}")
# Đóng phần insights}

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
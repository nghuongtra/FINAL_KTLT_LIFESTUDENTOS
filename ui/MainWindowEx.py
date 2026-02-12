import datetime
import random

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap

from model.comingevents import Upcomingevents
from model.task import Task
from model.tasks import Tasks
from ui.MainWindow import Ui_MainWindow
import ui.resources_rc

class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi((MainWindow))
        self.MainWindow = MainWindow
        self.tasks = Tasks()
        self.selectedTask=None
        self.tasks.import_json("../datasets/tasks.json")
        self.showTasksIntoQListWidget()


    def show(self):
        self.MainWindow.show()
        self.setupSignalAndSlot()
        self.stackedWidget.setCurrentIndex(0)
        self.updateCountdown()
        self.hien_thi_loi_khuyen_ngau_nhien()

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
    def updateinsight(self):
        text_GPA=self.lineEditGPA.text()
        if text_GPA == '':
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu GPA!\nVui lòng thử lại.")
            self.stackWidget.setCurrentIndex(1)
            return
        else:
            GPA=float(text_GPA)

        text_money=self.lineEditMoney.text()
        if text_money == '':
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu!\nVui lòng thử lại.")
            self.stackWidget.setCurrentIndex(2)
            return
        else:
            money=float(text_money)
        text_ns = self.lineEdit_NganSach.text()
        NGAN_SACH_BAN_DAU = float(text_ns)
        if NGAN_SACH_BAN_DAU/3 <= money:
            return baodong

        #Nhận xét
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
        if GPA >= 3.2 and money >= baodong:
            nhanxet = "Xuất sắc! Con nhà người ta đây rồi: Học giỏi - Tài chính vững!"
            tips=random.choice(tip_hoctot)

            # 2. HỌC GIỎI (>=3.2) + HẾT TIỀN
        elif GPA >= 3.2 and money < baodong:
            nhanxet = "Học tốt nha! Mà xài tiền hơi lố rồi đó, coi chừng cuối tháng ăn mì gói."
            self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
            tips =random.choice(tip_tietkiem)+random.choice(tip_hoctot)

            # 3. HỌC KHÁ/TRUNG BÌNH (<3.2) + TIỀN NHIỀU
        elif GPA < 3.2 and money >= baodong:
            nhanxet = "Tài chính rủng rỉnh nhưng việc học cần tập trung hơn nhé!"
            self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
            if GPA >= 2.5:
                nhanxet = "Học lực Khá! Bạn thử đổi phương pháp học xem sao!!"
                self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
            else:
                nhanxet = "Cảnh báo học tập! Đừng để tiền làm mờ mắt kiến thức."
                self.advice_2.setStyleSheet("background-color: yellow; color:black; font-weight:bold;")
            tips = random.choice(tip_caithien)

            # 4. HỌC KÉM + HẾT TIỀN
        else:
            nhanxet = "BÁO ĐỘNG ĐỎ: Cả Tiền và Điểm đều nguy cấp! Cần chấn chỉnh gấp!"
            self.advice_2.setStyleSheet("background-color: red; color:white; font-weight:bold;")
            tips = random.choice(tip_tietkiem)+random.choice(tip_caithien)
        self.advice_2.setText(nhanxet)
        self.input_tips.setText(tips)

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
            "shopping": 2500000,
            "food": 1500000,
            "study": 500000
        }
        if danh_sach_chi_tieu:
            # Tìm cái tiêu nhiều nhất
            top_cat = max(danh_sach_chi_tieu, key=danh_sach_chi_tieu.get)
            top_val = danh_sach_chi_tieu[top_cat]
            total_spend = sum(danh_sach_chi_tieu.values())

            percent = (top_val / total_spend) * 100 if total_spend > 0 else 0

            # Hiện phần trăm
            self.label_TopSpend_Percent.setText(f"{percent:.1f}%")  # <--- Thay tên label "%"

            # Hiện icon (Cần file ảnh trong thư mục images)
            icon_path = ""
            if top_cat == "shopping":
                icon_path = "../images/ic_shopping.png"
            elif top_cat == "food":
                icon_path = "../images/ic_food.png"
            elif top_cat == "study":
                icon_path = "../images/ic_study.png"

            if icon_path:
                self.label_TopSpend_Icon.setPixmap(QPixmap(icon_path))  # <--- Thay tên label Icon
                self.label_TopSpend_Icon.setScaledContents(True)










import datetime
import json
import os

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox, QInputDialog

from model.comingevents import Upcomingevents


class OverviewController:
    def __init__(self, main_view):
        self.view = main_view

    #########Tab overview
    def process_viewdetail(self):
        total_credits = 0
        total_weighted_score_10 = 0

        for item in self.view.sub_manager.list:
            credit = float(item.credit)
            score_final = (float(item.scoreProcess) * 0.3) + (float(item.scoreMidterm) * 0.2) + (float(item.scoreFinal) * 0.5)
            total_credits += credit
            total_weighted_score_10 += (score_final * credit)
        if total_credits > 0:
            avgScore = total_weighted_score_10 / total_credits
            gpa_4 = (avgScore / 10) * 4

            self.view.labelGPA.setText(f"{gpa_4:.2f}")
            self.view.labelGrade.setText(f"{avgScore:.2f}")
        else:
            self.view.labelGPA.setText("0.00")
            self.view.labelGrade.setText("Chưa có dữ liệu")

    def process_managefinance(self):
        total = self.view.label_total_3.text()
        self.view.labelTotal.setText(total)

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
        self.view.labelComingEvent.setText(f"Hôm nay: {today_display}\nSự kiện: {event_today}")

    def process_task(self):
        pending_count = 0
        overdue_count = 0
        now = datetime.datetime.now()
        for index in range(self.view.task_controller.tasks.size()):
            task = self.view.task_controller.tasks.item(index)

            if isinstance(task.deadline, str):
                task.deadline = datetime.date.fromisoformat(task.deadline)
            if isinstance(task.deadlinetime, str):
                task.deadlinetime = datetime.time.fromisoformat(task.deadlinetime)
            if not task.isfinish:
                pending_count += 1
                dt_deadline = datetime.datetime.combine(task.deadline, task.deadlinetime)
                if dt_deadline < now:
                    overdue_count += 1
        self.view.labelTaskPending.setText(str(pending_count))
        self.view.labelTaskOverdue.setText(str(overdue_count))
        if overdue_count > 0:
            self.view.labelTaskOverdue.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.view.labelTaskOverdue.setStyleSheet("color: green;")
    def openFB(self):
        # 1. Khởi tạo QDialog tùy chỉnh thay vì dùng hàm tĩnh
        dialog = QDialog(self.view.MainWindow)
        dialog.setWindowTitle("Góp ý / Liên hệ Admin")
        dialog.resize(400, 250)

        # 2. Áp dụng đoạn CSS của bạn (Tôi đổi QPlainTextEdit thành QTextEdit cho đồng bộ)
        dialog.setStyleSheet("""
                QDialog{
                    background-color:#FFF4CC;
                }

                QLabel{
                    font-size:14px;
                    color:#5A3E1B;
                    font-weight: bold;
                }

                QTextEdit{
                    background-color:white;
                    border:2px solid #E6B800;
                    border-radius:6px;
                    padding: 5px;
                    font-size: 13px;
                    color: black;
                }

                QPushButton{
                    background-color:#E6B800;
                    color:white;
                    padding:6px 15px;
                    border-radius:6px;
                    font-weight: bold;
                    min-width: 80px;
                }

                QPushButton:hover{
                    background-color:#d4a500;
                }
                """)

        # 3. Tạo bố cục (Layout)
        layout = QVBoxLayout(dialog)

        label = QLabel("Nhập nội dung góp ý của bạn:")
        layout.addWidget(label)

        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Gửi Góp Ý")
        btn_cancel = QPushButton("Hủy")

        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        # 4. Gắn sự kiện nút bấm
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        # 5. Mở hộp thoại và lưu data nếu bấm OK
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = text_edit.toPlainText()
            if text.strip():
                self.save_feedback(text.strip())

    def save_feedback(self, content):
        feedback_file = "../datasets/feedbacks.json"
        if not os.path.exists(feedback_file):
            with open(feedback_file, "w", encoding="utf-8") as f:
                json.dump({"feedbacks": []}, f)
        with open(feedback_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        now = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
        username = getattr(self.view, "current_acc", "Unknown_User")

        new_feedback = {
            "username": username,
            "time": now,
            "content": content
        }
        data["feedbacks"].append(new_feedback)

        # 4. Ghi đè lại vào file JSON
        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        QMessageBox.information(
            self.view.MainWindow,
            "Thành công",
            "Cảm ơn bạn đã gửi góp ý cho Admin!"
        )
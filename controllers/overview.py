import datetime

from model.comingevents import Upcomingevents


class OverviewController:
    def __init__(self, main_view):
        self.view = main_view

    #########Tab overview
    def process_viewdetail(self):
        total_credits = 0
        total_weighted_score_10 = 0
        for item in self.view.sub_manager.list:
                credit = int(item.credit)
                score_final = float(item.scoreFinal)
                total_credits += credit
                total_weighted_score_10 += (score_final * credit)
        if total_credits > 0:
            avgScore = total_weighted_score_10 / total_credits
            gpa_4 = (avgScore/ 10) * 4

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
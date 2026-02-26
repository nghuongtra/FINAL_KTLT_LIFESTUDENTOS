import datetime

from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox

from model.task import Task
from model.tasks import Tasks


class TaskController:
    def __init__(self, main_view):
        self.view = main_view
        self.tasks = Tasks()
        self.selectedTask = None
    def setup(self):
        self.tasks.import_json("../datasets/tasks.json")
        self.showTasksIntoQListWidget()

    # { Phần của tab task scheduler

    def showTasksIntoQListWidget(self):
        self.view.listWidgetTask.clear()
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
            self.view.listWidgetTask.addItem(item)
            if not task.isfinish:
                dt_deadline = datetime.datetime.combine(task.deadline, task.deadlinetime)
                dt_now = datetime.datetime.now()
                diff = (dt_deadline - dt_now).total_seconds()  # tính khoảng cách thời gian cho labelcountdown
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
        self.view.lineEditTitle.setText("")
        self.view.textEditContent.setText("")
        self.view.dateEditDeadline.setSpecialValueText(None)
        self.view.radioButtonFinished.setAutoExclusive(False)
        self.view.radioButtonNotFinished.setAutoExclusive(False)
        self.view.radioButtonFinished.setChecked(False)
        self.view.radioButtonNotFinished.setChecked(False)
        self.view.radioButtonFinished.setAutoExclusive(True)
        self.view.radioButtonNotFinished.setAutoExclusive(True)
        self.selectedTask = None
        self.view.lineEditTitle.setFocus()

    def processSave(self):
        title = self.view.lineEditTitle.text()
        content = self.view.textEditContent.toPlainText()
        date = self.view.dateEditDeadline.date().toPyDate()
        time = self.view.timeEditDeadline.time().toPyTime()
        isFinished = self.view.radioButtonFinished.isChecked()
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
            self.view.MainWindow,
            'Xác nhận',
            'Bạn có chắc chắn muốn xóa công việc này không?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.No:
            return
        size = self.view.listWidgetTask.count()
        for index in range(size - 1, -1, -1):
            item = self.view.listWidgetTask.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                self.tasks.removeByIndex(index)
        self.selectedTask = None
        self.showTasksIntoQListWidget()
        self.tasks.export_json("../datasets/tasks.json")

    def processItemSelection(self):
        row = self.view.listWidgetTask.currentRow()
        if row < 0:
            return
        task = self.tasks.item(row)
        self.view.lineEditTitle.setText(task.title)
        self.view.textEditContent.setText(task.content)
        self.view.dateEditDeadline.setDate(task.deadline)
        self.view.timeEditDeadline.setTime(task.deadlinetime)
        if task.isfinish:
            self.view.radioButtonFinished.setChecked(True)
            self.view.radioButtonNotFinished.setChecked(False)
        else:
            self.view.radioButtonFinished.setChecked(False)
            self.view.radioButtonNotFinished.setChecked(True)
        self.selectedTask = task

    def updateCountdown(self):
        q_date = self.view.dateEditDeadline.date()
        q_time = self.view.timeEditDeadline.time()
        deadline_qdt = QDateTime(q_date, q_time)
        now_qdt = QDateTime.currentDateTime()
        seconds_diff = now_qdt.secsTo(deadline_qdt)
        if seconds_diff < 0:
            self.view.labelCountdown.setText("Đã quá hạn!")
            self.view.labelCountdown.setStyleSheet("color: red; font-weight: bold;")
        else:
            days = seconds_diff // 86400
            hours = (seconds_diff % 86400) // 3600
            minutes = (seconds_diff % 3600) // 60
            self.view.labelCountdown.setText(f"Còn: {days} ngày, {hours} giờ, {minutes} phút")
            self.view.labelCountdown.setStyleSheet("color: blue; font-weight: bold;")
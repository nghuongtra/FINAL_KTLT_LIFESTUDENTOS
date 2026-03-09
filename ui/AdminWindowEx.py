from PyQt6.QtWidgets import QMessageBox, QMainWindow


from ui.AdminWindow import Ui_MainWindow


class AdminWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlots()

    def show(self):
        self.MainWindow.show()

    def setupSignalAndSlots(self):
        pass



from ui.MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi((MainWindow))
        self.MainWindow = MainWindow

    def show(self):
        self.MainWindow.show()
        self.setupSignalAndSlot()
        self.stackedWidget.setCurrentIndex(0)

    def setupSignalAndSlot(self):
        self.pushButtonOverview.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButtonAcademic.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButtonFinanceManagement.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButtonTaskScheduler.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButtonInsights.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))


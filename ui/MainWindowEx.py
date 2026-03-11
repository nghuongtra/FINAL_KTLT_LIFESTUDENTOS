from PyQt6 import QtGui, QtWidgets

from controllers.academic import AcademicController
from controllers.finance import FinanceController
from controllers.insight import InsightController
from controllers.overview import OverviewController
from controllers.task import TaskController
from ui.MainWindow import Ui_MainWindow
import resources_rc

class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi((MainWindow))
        self.MainWindow = MainWindow

#TAB 2:
        self.academic_controller = AcademicController(self)
        self.academic_controller.current_acc = self.current_acc
        self.academic_controller.setup()
        self.sub_manager = self.academic_controller.sub_manager
#TAB 3
        self.finance_controller = FinanceController(self)

        self.finance_controller.current_acc = self.current_acc
        self.finance_controller.setup()
        self.expense_manager = self.finance_controller.expense_manager
        self.balance_manager = self.finance_controller.balance_manager
#TAB 4
        self.task_controller = TaskController(self)
        self.task_controller.current_acc = self.current_acc
        self.task_controller.setup()
#TAB 5
        self.insight_controller = InsightController(self)
        self.insight_controller.current_acc = self.current_acc

#Overview
        self.overview_controller = OverviewController(self)
        self.overview_controller.current_acc = self.current_acc


    def show(self):
        self.MainWindow.show()
        self.setupSignalAndSlot()
        self.stackedWidget.setCurrentIndex(0)
        self.task_controller.updateCountdown()

    def setupSignalAndSlot(self):
        #liên kết các nút bấm trên header với các page
        self.pushButtonOverview.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButtonAcademic.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButtonFinanceManagement.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButtonTaskScheduler.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButtonInsights.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pageInsight))
        #Overview
        self.pushButtonViewDetail.clicked.connect(self.overview_controller.process_viewdetail)
        self.pushButtonManageFinances.clicked.connect(self.overview_controller.process_managefinance)
        self.pushButtonViewCalendar.clicked.connect(self.overview_controller.process_calendar)
        self.pushButtonViewTask.clicked.connect(self.overview_controller.process_task)
        self.pushButtonGopy.clicked.connect(self.overview_controller.openFB)
        #Phần của tab task
        self.pushButtonNew.clicked.connect(self.task_controller.processNew)
        self.pushButtonSave.clicked.connect(self.task_controller.processSave)
        self.pushButtonDeleteTask.clicked.connect(self.task_controller.processRemove)
        self.listWidgetTask.itemSelectionChanged.connect(self.task_controller.processItemSelection)
        self.dateEditDeadline.dateChanged.connect(self.task_controller.updateCountdown)
        self.timeEditDeadline.timeChanged.connect(self.task_controller.updateCountdown)

#TAB 2:
        self.pushButtonCalculateGPA.clicked.connect(self.academic_controller.process_calculate_gpa)
        self.pushButtonAddSubject.clicked.connect(self.academic_controller.process_add_subject)
        self.pushButtonEdit.clicked.connect(self.academic_controller.process_edit_subject)
        self.pushButtonDelete.clicked.connect(self.academic_controller.process_delete_subject)
        self.tableWidgetthongtinmon.itemSelectionChanged.connect(self.academic_controller.process_selection)
        self.lineEditTimmon.textChanged.connect(self.academic_controller.search_subject)
        self.tableWidgetthongtinmon.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

#TAB 3
        self.pushButtonAddExpense.clicked.connect(self.finance_controller.TAB3_PROCESS_ADD)
        self.pushButton_addincome.clicked.connect(self.finance_controller.TAB3_PROCESS_ADD_INCOME)
        self.pushButtonsearch_3.clicked.connect(self.finance_controller.TAB3_PROCESS_RIGHT_TABLE)
        self.comboBoxsapxep_2.currentIndexChanged.connect(self.finance_controller.TAB3_PROCESS_RIGHT_TABLE)
        self.comboBoxloc_2.currentIndexChanged.connect(self.finance_controller.TAB3_PROCESS_RIGHT_TABLE)

# OVERSIGHT & INSIGHTS
        self.pushButtonInsights.clicked.connect(self.insight_controller.updateinsight)
        self.xuatfileexcel.clicked.connect(self.insight_controller.process_excel_csv)
        self.stackedWidget.currentChanged.connect(self.insight_controller.kiem_tra_trang_hien_tai)
        if hasattr(self, 'lineEditInputGPA'):
            self.lineEditInputGPA.setReadOnly(True)
            self.lineEditInputGPA.setPlaceholderText("Đang tính...")
        if hasattr(self, 'lineEditInputTienDo'):
            self.lineEditInputTienDo.setPlaceholderText("Đang tính...")
            self.lineEditInputTienDo.setReadOnly(True)
        if hasattr(self, 'lineEditInputTienDo_2'):
            self.lineEditInputTienDo_2.setPlaceholderText("Đang tính...")
            self.lineEditInputTienDo_2.setReadOnly(True)

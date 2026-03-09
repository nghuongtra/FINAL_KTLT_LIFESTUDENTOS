
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.AdminWindowEx import AdminWindowEx

app=QApplication([])
myWindow=AdminWindowEx()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()
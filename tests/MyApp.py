
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.LoginWindowEx import LoginWindowEx


app=QApplication([])
myWindow=LoginWindowEx()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()
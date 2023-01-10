import sys
from PyQt5.QtWidgets import QApplication
from ui import UserInterface

app = QApplication(sys.argv)
ui = UserInterface()
ui.show()
#sys.exit(app.exec_())

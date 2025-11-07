import sys
from PyQt5.QtWidgets import QApplication
from login_ui import Ui_Log_in
from DatabaseConnection import DatabaseConnection

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DatabaseConnection()
    ventana = Ui_Log_in()
    ventana.showMaximized()
    sys.exit(app.exec_())

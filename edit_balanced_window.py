from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QPushButton
)
import sys
from main import load_language_config
from api import get_accounts

class edit_balanced_window(QDialog):

    def __init__(self):
        super().__init__()
        # Api Request Results
        self.api_request = get_accounts()
        self.api_request_message = self.api_request.get("message", "Message Error")
        print(self.api_request_message)
        self.api_accounts = self.api_request.get("accounts", [])

        
        layout = QVBoxLayout(self)

        self.label = QLabel("Edit Balanced Window")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(5)
        # Languages
        self.name_current_account_Balance_text = text_config.get("current_account_balance", "Error Name for Current Account Balance")
        self.update_current_account_button_text = text_config.get("update_current_account_button", "Error Name for Update Current Account Button")

        self.table.setHorizontalHeaderLabels(["Name", self.name_current_account_Balance_text, self.update_current_account_button_text])
        self.table.setItem(0, 0, QTableWidgetItem("Beispiel Name 1"))
        self.table.setItem(0, 1, QTableWidgetItem("1000"))
        update_button = QPushButton(self.update_current_account_button_text)
        self.table.setCellWidget(0, 2, update_button)
        self.table.setVerticalHeaderLabels([str(i+1) for i in range(5)])
        layout.addWidget(self.table)





if __name__ == '__main__':
    global text_config
    # Debugging delete After Usage
    language = "EN"
    text_config = load_language_config("text_translate.txt", language)
    app = QApplication(sys.argv)
    window = edit_balanced_window()
    window.show()
    app.exec()
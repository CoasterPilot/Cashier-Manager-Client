from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView
)
import sys
from main import load_language_config
from api import get_accounts
from PySide6.QtCore import Qt

from globals import language

class edit_balanced_window(QDialog):

    def __init__(self):
        super().__init__()
        text_config = load_language_config("text_translate.txt", language)
        # Api Request Results
        self.api_request = get_accounts()
        self.api_request_message = self.api_request.get("message", "Message Error")
        print(self.api_request_message)
        self.api_accounts = self.api_request.get("accounts", [])
        standard_window_height = 100
        # Multiplikator Pro Nutzer
        user_height = 35
        windowrange = 0
        for number in range(len(self.api_accounts)):
            windowrange += user_height
        windowheight = standard_window_height + windowrange
        print(windowrange)
        # Window Settings
        window_title = text_config.get("edit_balance_window_title", "Error Name for Edit Balanced Window")
        self.setWindowTitle(window_title)
        self.setGeometry(100, 100, 400, windowheight)
        
        layout = QVBoxLayout(self)


        # Abfrage wie viele Konten vorhanden sind und diese in Tabelle anzeigen
        num_accounts = len(self.api_accounts)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(num_accounts)
        # Languages
        self.name_current_account_Balance_text = text_config.get("current_account_balance", "Error Name for Current Account Balance")
        self.update_current_account_button_text = text_config.get("update_current_account_button", "Error Name for Update Current Account Button")

        self.table.setHorizontalHeaderLabels(["Name", self.name_current_account_Balance_text, self.update_current_account_button_text])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)          # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Kontostand
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Update-Button
        #Setze Name für Benutuzer und Kontostand aus API Request
        
        for i in range(len(self.api_accounts)):
            #Benutzer
            benutzername = self.api_accounts[i][0]
            userid = self.api_accounts[i][2]
            self.table.setItem(i, 0, QTableWidgetItem(benutzername))
            #Kontostand abfragen
            kontostand = self.api_accounts[i][1]
            item = QTableWidgetItem(str(kontostand))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 1, item)
            update_button = QPushButton(self.update_current_account_button_text)
            update_button.clicked.connect(lambda checked, userid=userid: self.open_change_balance_window(userid))  # Hier kannst du die Funktion zum Aktualisieren des Kontostands hinzufügen
            self.table.setCellWidget(i, 2, update_button)
        self.table.setVerticalHeaderLabels([str(i+1) for i in range(num_accounts)])
        layout.addWidget(self.table)
        self.reload_window_button = QPushButton("Reload Window")
        self.reload_window_button.clicked.connect(self.reload_window)
        layout.addWidget(self.reload_window_button)
        self.close_button_text = text_config.get("close_button_text", "Error Name for Close Button")
        self.close_button = QPushButton(self.close_button_text)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

    def open_change_balance_window(self, userid):
        from change_account_balance_window import change_account_balance_window
        self.change_balance_window = change_account_balance_window(userid)
        self.change_balance_window.exec()
        self.reload_window()

    def reload_window(self):
        self.close()

        self.new_window = edit_balanced_window()
        self.new_window.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = edit_balanced_window()
    window.show()
    app.exec()
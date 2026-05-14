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

global text_config
# Debugging delete After Usage
language = "EN"
text_config = load_language_config("text_translate.txt", language)

class edit_balanced_window(QDialog):

    def __init__(self):
        super().__init__()
        # Api Request Results
        self.api_request = get_accounts()
        self.api_request_message = self.api_request.get("message", "Message Error")
        print(self.api_request_message)
        self.api_accounts = self.api_request.get("accounts", [])
        standard_window_height = 100
        # Multiplikator Pro Nutzer
        user_height = 30
        windowrange = 0
        for number in range(len(self.api_accounts)):
            windowrange += user_height
        windowheight = standard_window_height + windowrange
        print(windowrange)
        self.setGeometry(100, 100, 400, windowheight)
        
        layout = QVBoxLayout(self)

        self.label = QLabel("Edit Balanced Window")
        layout.addWidget(self.label)

        # Abfrage wie viele Konten vorhanden sind und diese in Tabelle anzeigen
        num_accounts = len(self.api_accounts)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(num_accounts)
        # Languages
        self.name_current_account_Balance_text = text_config.get("current_account_balance", "Error Name for Current Account Balance")
        self.update_current_account_button_text = text_config.get("update_current_account_button", "Error Name for Update Current Account Button")

        self.table.setHorizontalHeaderLabels(["Name", self.name_current_account_Balance_text, self.update_current_account_button_text])
        #Setze Name für Benutuzer und Kontostand aus API Request
        
        for i in range(len(self.api_accounts)):
            #Benutzer
            benutzername = self.api_accounts[i][0]
            self.table.setItem(i, 0, QTableWidgetItem(benutzername))
            #Kontostand abfragen
            kontostand = self.api_accounts[i][1]
            self.table.setItem(i, 1, QTableWidgetItem(str(kontostand)))
            update_button = QPushButton(self.update_current_account_button_text)
            update_button.clicked.connect(lambda checked, name=benutzername, buttonnumber=i: print(f"Benutzername: {name}. Number: {buttonnumber}"))  # Hier kannst du die Funktion zum Aktualisieren des Kontostands hinzufügen
            self.table.setCellWidget(i, 2, update_button)
        self.table.setVerticalHeaderLabels([str(i+1) for i in range(num_accounts)])
        layout.addWidget(self.table)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = edit_balanced_window()
    window.show()
    app.exec()
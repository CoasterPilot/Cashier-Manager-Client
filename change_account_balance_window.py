import sys
from PySide6.QtWidgets import (
    QDialog,
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)
from main import load_language_config


class change_account_balance_window(QDialog):

    def __init__(self, userid):
        super().__init__()
        global text_config
        language = "EN"
        text_config = load_language_config("text_translate.txt", language)
        
        # get Account data for Token

        from api import get_account_data
        account_data = get_account_data(userid)
        username = account_data.get("username", "Error Username")
        current_balance = account_data.get("cash_balance", "Error Balance")
        account_id = account_data.get("account_id", "Error User ID")


        # Screen size
        w = 500
        h = 500

        # get Screen Size
        screen = QApplication.primaryScreen().geometry()

        # Calculate middle of the Screen
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2

        # Set Layout

        layout = QVBoxLayout()


        # Set Window in the Middle of the Screen
        self.setGeometry(x, y, w, h)
        window_titel_text = text_config.get("change_account_balance_window_title", "Error cant find Title for Change Account Window")
        self.setWindowTitle(window_titel_text + " " + username)

        # Set text_how_much_do_you_want_to_pay text field

        text_how_much_do_you_want_to_pay = text_config.get("text_how_much_do_you_want_to_pay", "Error cant find Text for How Much Do You Want To Pay")
        text_current_account_balance = text_config.get("current_account_balance", "Error cant find Text for Current Account Balance")
        self.label_how_much_do_you_want_to_pay = QLabel(text_current_account_balance + " " + str(current_balance) + "€. " + text_how_much_do_you_want_to_pay)
        self.label_how_much_do_you_want_to_pay.setGeometry(50, 50, 400, 30)
        self.label_how_much_do_you_want_to_pay.setParent(self)
        layout.addWidget(self.label_how_much_do_you_want_to_pay)
        

        # Pay Field

        pay_field = QLineEdit()
        pay_field.setFixedWidth(200) 
        pay_field.setParent(self)
        layout.addWidget(pay_field)


        # Reason for Paying Label

        reason_for_paying_text = text_config.get("reason_for_paying_text", "Error cant find Text for Reason For Paying")
        self.label_reason_for_paying = QLabel(reason_for_paying_text)
        self.label_reason_for_paying.setParent(self)
        layout.addWidget(self.label_reason_for_paying)

        # Reason for Paying Field
        reason_for_paying_field = QLineEdit()
        reason_for_paying_field.setFixedWidth(200)
        reason_for_paying_field.setParent(self)
        layout.addWidget(reason_for_paying_field)


        # Pay Button
        pay_button_text = text_config.get("pay_button_text", "Error cant find Text for Pay Button")
        pay_button = QPushButton(pay_button_text)
        pay_button.setFixedWidth(200)
        pay_button.setParent(self)
        pay_button.clicked.connect(lambda: self.pay_over_api(account_id, value=pay_field.text(), reason=reason_for_paying_field.text(), username_creator=username))
        layout.addWidget(pay_button)

        # Close Button
        close_button_text = text_config.get("close_button_text", "Error cant find Text for Close Button")
        close_button = QPushButton(close_button_text)
        close_button.clicked.connect(self.close)
        close_button.setFixedWidth(200)
        close_button.setParent(self)
        layout.addWidget(close_button)

        # setlayout
        layout.addStretch()
        self.setLayout(layout)


    def pay_over_api(self, account_id, value, reason, username_creator):
        print("Pay Button Clicked. user_id: " + str(account_id) + "Value: " + value + " Reason: " + reason)
        from api import update_balance
        
        response = update_balance(account_id, value, reason, username_creator)
        print(response)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    global language
    language = "EN"
    global text_config
    text_config = load_language_config("text_translate.txt", language)

    window = change_account_balance_window(token="example_token")
    window.show()
    sys.exit(app.exec())


import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout
)
from functions import *



def load_language_config(filename, language):
    data = {}
    current_section = None

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            # neue Sektion
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                continue

            if current_section == language:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()

    return data



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Show 
        from globals import language
        global text_config
        text_config = load_language_config("text_translate.txt", language)
        self.button_edit_balance_text = text_config.get("button_open_edit_window", "Error Name for Pay Page")
        self.button_edit_balance = QPushButton(self.button_edit_balance_text)
        self.button_edit_balance.clicked.connect(self.show_edit_balanced_window)
        self.button_add_food_text = text_config.get("button_open_add_food_window", "Error Name for Add Food Page")
        self.button_add_food = QPushButton(self.button_add_food_text)
        self.button_add_food.clicked.connect(self.show_add_food_window)
        self.button_logout = QPushButton("Logout (Deactivated)")
        #self.button_logout.clicked.connect()
        # Zentrales Widget erstellen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Vertikales Layout
        layout = QVBoxLayout(central_widget)

        # Buttons hinzufügen
        layout.addWidget(self.button_edit_balance)
        layout.addWidget(self.button_add_food)
        self.w = None

    #def show_edit_balanced_window(self, checked):
    def show_edit_balanced_window(self):
        from edit_balanced_window import edit_balanced_window
        self.w = edit_balanced_window()
        self.w.exec()

    def show_add_food_window(self):
        from new_food_window import new_food_window
        self.w = new_food_window()
        self.w.exec()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
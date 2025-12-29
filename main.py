import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton
)


def read_config_value(filename, key):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # leere Zeilen oder Kommentare überspringen
            if not line or line.startswith("#"):
                continue

            if line.startswith(key + "="):
                return line.split("=", 1)[1].strip()

    return None


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
        text_config = load_language_config("sample_text_translate.txt", language)
        self.button_edit_balance_text = text_config.get("button_open_edit_window", "Error Name for Pay Page")
        self.button_edit_balance = QPushButton(self.button_edit_balance_text)
        self.button_edit_balance.clicked.connect(self.show_edit_balanced_window)
        self.button_logout = QPushButton("Logout (Deactivated)")
        #self.button_logout.clicked.connect()
        self.setCentralWidget(self.button_edit_balance)
        self.w = None

    #def show_edit_balanced_window(self, checked):
    def show_edit_balanced_window(self):
        if self.w is None:
            from edit_balanced_window import edit_balanced_window
            self.w = edit_balanced_window()
        self.w.exec()


if __name__ == '__main__':
    global language
    language = read_config_value("config.txt", "Language")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
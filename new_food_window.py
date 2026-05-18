from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QApplication,
)
import sys


class new_food_window(QDialog):

    def __init__(self):
        super().__init__()

        # Window Init
        self.setWindowTitle("New Food Window")
        self.setGeometry(100, 100, 400, 300)

        # MAIN LAYOUT
        self.layout = QVBoxLayout(self)

        # STATIC UI
        self.label_amount_of_invoice = QLabel("Amount of Invoice")
        self.dropdown = QComboBox()

        for i in range(10):
            self.dropdown.addItem(str(i))

        self.dropdown.currentTextChanged.connect(self.generate_gui)

        self.layout.addWidget(self.label_amount_of_invoice)
        self.layout.addWidget(self.dropdown)

        # dynamic UI
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)


        self.layout.addStretch()

        self.created_elements_list = []

    # Generate GUI for Amount of Invoice
    def generate_gui(self, text):
        print("You picked:", text)

        # delete old elements
        for element in self.created_elements_list:
            element.deleteLater()

        self.created_elements_list = []

        # new elements only in the content layout
        for number in range(int(text)):
            label = QLabel(f"Invoice {number + 1}")
            text_box = QLineEdit()

            self.created_elements_list.append(label)
            self.created_elements_list.append(text_box)

            self.content_layout.addWidget(label)
            self.content_layout.addWidget(text_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = new_food_window()
    window.show()
    sys.exit(app.exec())
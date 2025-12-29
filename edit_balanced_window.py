from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QApplication
)
import sys

class edit_balanced_window(QDialog):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Edit Balanced Window")
        layout.addWidget(self.label)
        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = edit_balanced_window()
    window.show()
    app.exec()
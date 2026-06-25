from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QApplication,
    QPushButton
)
import sys
from functions import get_users
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from functions import Text_Only_Float_Validator

float_validator = Text_Only_Float_Validator()

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

        # Create Lists
        self.created_elements_list = []
        self.created_name_fields_elements_list = []
        self.invoice_fields = []

        self.user_list = get_users()

    # Generate GUI for Amount of Invoice
    def generate_gui(self, text):
        print("You picked:", text)
        self.invoice_fields.clear()

        # delete old elements
        for element in self.created_elements_list:
            element.deleteLater()
        self.created_elements_list.clear()
        for element in self.created_name_fields_elements_list:
            element.deleteLater()
        self.created_name_fields_elements_list.clear()


        self.created_elements_list.clear()

        # Generate Invoice Elements
        for number in range(int(text)):
            label = QLabel(f"Invoice {number + 1}")
            text_box = QLineEdit()
            text_box.setValidator(float_validator)
            who_payd_the_invoice_label = QLabel("Who pay the Invoice?")
        
            who_payd_the_invoice_text_box = QComboBox()
            #Change it to Users Via API Request
            for user in self.user_list:
                who_payd_the_invoice_text_box.addItem(user)

            # SAFE Invoice with Name
            invoice = {
                "price": text_box,
                "paid_by": who_payd_the_invoice_text_box
            }
            self.invoice_fields.append(invoice)


            self.created_elements_list.append(label)
            self.created_elements_list.append(text_box)
            self.created_elements_list.append(who_payd_the_invoice_label)
            self.created_elements_list.append(who_payd_the_invoice_text_box)

            self.content_layout.addWidget(label)
            self.content_layout.addWidget(text_box)
            self.content_layout.addWidget(who_payd_the_invoice_label)
            self.content_layout.addWidget(who_payd_the_invoice_text_box)



        # add Name of the Food
        if text != "0":
            name_of_food_label = QLabel("Name of the Food")
            self.name_of_food_text_box = QLineEdit()
            Number_of_eating_people_label = QLabel("Number of Eating People")
            self.Number_of_eating_people_combobox = QComboBox()
            for i in range(10):
                self.Number_of_eating_people_combobox.addItem(str(i))
            self.created_elements_list.append(self.Number_of_eating_people_combobox)
            self.created_elements_list.append(Number_of_eating_people_label)
            self.created_elements_list.append(name_of_food_label)
            self.created_elements_list.append(self.name_of_food_text_box)
            self.content_layout.addWidget(name_of_food_label)
            self.content_layout.addWidget(self.name_of_food_text_box)
            self.Number_of_eating_people_combobox.currentTextChanged.connect(self.create_name_fields)
            self.content_layout.addWidget(Number_of_eating_people_label)
            self.content_layout.addWidget(self.Number_of_eating_people_combobox)

        else:
            pass
        

    def create_name_fields(self, number_of_people):
        print("Number of People:", number_of_people)
        self.eating_people_name_fields = []
        for element in self.created_name_fields_elements_list:
            element.deleteLater()
        self.created_name_fields_elements_list.clear()
        for number in range(int(number_of_people)):
            name_of_eating_person_label = QLabel(f"Name of the Eating Person {number + 1}")
            name_of_eating_person_text_box = QComboBox()
            for user in self.user_list:
                name_of_eating_person_text_box.addItem(user)
            self.created_name_fields_elements_list.append(name_of_eating_person_label)
            self.created_name_fields_elements_list.append(name_of_eating_person_text_box)
            self.content_layout.addWidget(name_of_eating_person_label)
            self.content_layout.addWidget(name_of_eating_person_text_box)
            self.eating_people_name_fields.append(name_of_eating_person_text_box)
        
        # add calculate button

        if number_of_people != "0":
            calculate_button = QPushButton("Calculate")
            calculate_button.clicked.connect(self.calculate_price)
            self.created_name_fields_elements_list.append(calculate_button)
            self.content_layout.addWidget(calculate_button)
        else:
            pass

    def calculate_price(self):
        pay_list = []
        food_name = self.name_of_food_text_box.text()
        all_invoice_prices_list = []
        print("Calculate Price Button Clicked")
        # Api Request to Calculate Price
        # Get all the Data from the Fields and send it to the API
        #First get the Price and the Person who payd the Invoice
        for index, invoice in enumerate(self.invoice_fields):
            temp_name_pay_amount_list = {}
            price = invoice["price"].text()
            person = invoice["paid_by"].currentText()
            if price and person:
                print(
                    f"Invoice {index+1}:",
                    "Preis:", price,
                    "Bezahlt von:", person
                )
                #Calculate Negfative Price for API Request
                negative_price = -abs(float(price))
                temp_name_pay_amount_list["price"] = negative_price
                temp_name_pay_amount_list["paid_by"] = person
                pay_list.append(temp_name_pay_amount_list)
                all_invoice_prices_list.append(float(price))
                print("Pay List:", pay_list)
        # Price Per Person Calculation
            else:
                print(f"Invoice {index+1} is missing price or person information.")
                return  # Stop calculation if any invoice is incomplete
        price_per_person = sum(all_invoice_prices_list) / len(self.eating_people_name_fields)
        print("Price Per Person:", price_per_person)

        for index, names in enumerate(self.eating_people_name_fields):
            if names.currentText():
                temp_name_pay_amount_list = {}
                person_name = self.eating_people_name_fields[index].currentText()
                temp_name_pay_amount_list["price"] = price_per_person
                temp_name_pay_amount_list["paid_by"] = person_name
                pay_list.append(temp_name_pay_amount_list)

            else:
                print(f"Name of Eating Person {index+1} is missing.")
                return  # Stop calculation if any name is missing


     
        print("test")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = new_food_window()
    window.show()
    sys.exit(app.exec())
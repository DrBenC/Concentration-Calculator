import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QPushButton, QGridLayout, QLineEdit
from PyQt6.QtGui import QIcon

class chemical:
    def __init__(self, name, weight, density):
        self.name = name
        self.weight = weight
        self.density = density
        self.is_solid = True if (density == "SOLID") else False

class main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.chemicals_list = update_chemical_list()
        self.mass = 0
        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass

        self.setGeometry(100, 100, 600, 80)
        self.setStyleSheet('.QLabel { font-size: 14pt;}')
        self.setWindowTitle("Concentration Calculator")
        layout = QGridLayout()

        self.chemicals_cb = QComboBox()
        update_cb(self.chemicals_cb, self.chemicals_list)
        font = self.chemicals_cb.font()
        font.setPointSize(14)
        self.chemicals_cb.setEditable(False)
        self.chemicals_cb.setFont(font)
        self.chemicals_cb.currentIndex()

        self.weight_label = QLabel(f"  {self.chemicals_list[0].weight} Da")
        self.current_molecular_weight = self.chemicals_list[0].weight

        self.molar_input = QLineEdit(self)
        self.molar_input.setFixedWidth(300)
        font_input = self.molar_input.font()
        font_input.setPointSize(14)
        self.molar_input.setFont(font_input)

        self.molar_multiplier = QComboBox()
        self.molar_multiplier.setFont(font)

        self.molar_multiplier.setEditable(False)
        self.molar_multiplier.setFont(font)
        self.molar_multiplier.addItems(["umol", "mmol", "mol", "kmol"])

        self.masses = ["ug", "mg", "g", "kg"]
        self.mass_multiplier = QComboBox()
        self.mass_multiplier.setFont(font)

        self.mass_multiplier.setEditable(False)
        self.mass_multiplier.setFont(font)
        self.mass_multiplier.addItems(self.masses)
        self.multipliers = [0.001, 1, 1000, 1000000]

        self.result_label = QLabel("")

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFont(font)
        self.calculate_button.clicked.connect(self.calculate_mass)

        self.output_title = QLabel(" ")
        self.output_label = QLabel(" ")

        self.storage_1 = QLabel(" ")
        self.storage_1_button = QPushButton("Store Value")
        self.storage_1_button.setFont(font)
        self.storage_1_button.clicked.connect(self.store_1)

        self.storage_2 = QLabel(" ")
        self.storage_2_button = QPushButton("Store Value")
        self.storage_2_button.setFont(font)
        self.storage_2_button.clicked.connect(self.store_2)

        self.new_name = QLineEdit(self)
        self.new_name.setFixedWidth(300)
        self.new_name.setFont(font_input)

        self.new_molar_mass = QLineEdit(self)
        self.new_molar_mass.setFixedWidth(300)
        self.new_molar_mass.setFont(font_input)

        self.add_chemical_button = QPushButton("Add Chemical")
        self.add_chemical_button.setFont(font)
        self.add_chemical_button.clicked.connect(self.add_chemical)


        layout.addWidget(QLabel("Species:"), 0,0)
        layout.addWidget(self.chemicals_cb, 0, 1)
        layout.addWidget(self.weight_label, 0, 2)
        layout.addWidget(QLabel("Molar Amount:"), 1, 0)
        layout.addWidget(self.molar_input, 1, 1)
        layout.addWidget(self.molar_multiplier, 1, 2)
        layout.addWidget(QLabel("Result Units:"), 2, 0)
        layout.addWidget(self.mass_multiplier, 2, 2)
        layout.addWidget(self.calculate_button, 3, 2)
        layout.addWidget(self.output_title, 3, 0)
        layout.addWidget(self.output_label, 3, 1)
        layout.addWidget(self.storage_1, 4, 0,1,2)
        layout.addWidget(self.storage_1_button,4,2)
        layout.addWidget(self.storage_2, 5, 0,1,2)
        layout.addWidget(self.storage_2_button,5,2)
        layout.addWidget(QLabel(" "), 6, 0)
        layout.addWidget(QLabel("Add new chemical to list:"), 7, 0, 1, 2)
        layout.addWidget(QLabel("Name:"), 8, 0)
        layout.addWidget(self.new_name, 8, 1)
        layout.addWidget(QLabel("Molar Mass:"), 9, 0)
        layout.addWidget(self.new_molar_mass, 9, 1)
        layout.addWidget(self.add_chemical_button, 9, 2)

        self.setLayout(layout)
        self.chemicals_cb.currentIndexChanged.connect(self.update_weight_label)

    def update_weight_label(self, i):
        self.chemicals_list = update_chemical_list()
        self.weight_label.setText("   ")
        self.molecular_weight = self.chemicals_list[i].weight
        self.weight_label.setText(f"  {self.molecular_weight} Da")
        return self.molecular_weight

    def calculate_mass(self):
        if is_number(self.molar_input.text()) == True:
            self.mass = 0.0
            self.current_molecular_weight = float(self.chemicals_list[self.chemicals_cb.currentIndex()].weight)
            self.multiplier_molar = self.multipliers[self.molar_multiplier.currentIndex()]
            self.multiplier_mass = self.multipliers[self.mass_multiplier.currentIndex()]
            self.mass = round(float(self.current_molecular_weight)*float(self.molar_input.text())*self.multiplier_molar/self.multiplier_mass, 2)
            self.output_title.setText("Mass:")
            self.output_label.setText(f"{self.mass} {self.masses[self.mass_multiplier.currentIndex()]}")

        else:
            self.output_title.setText(f" ")
            self.output_label.setText(f"Input numeric value")

    def store_1(self):
        self.calculate_mass()
        if type(self.mass) == float:
            self.chemical = self.chemicals_list[self.chemicals_cb.currentIndex()].name
            self.molar_units = self.molar_multiplier.currentText()
            self.storage_1.setText(f"{self.molar_input.text()} {self.molar_units} {self.chemical} - {self.mass} {self.mass_multiplier.currentText()}")

    def store_2(self):
        self.calculate_mass()
        if type(self.mass) == float:
            self.chemical = self.chemicals_list[self.chemicals_cb.currentIndex()].name
            self.molar_units = self.molar_multiplier.currentText()
            self.storage_2.setText(
                f"{self.molar_input.text()} {self.molar_units} {self.chemical} - {self.mass} {self.mass_multiplier.currentText()}")

    def add_chemical(self):
        with open("chemicals_list.txt", "a") as f:
           f.write(f"\n{self.new_name.text()},{float(self.new_molar_mass.text())},SOLID")
        self.chemicals_list = update_chemical_list()
        update_cb(self.chemicals_cb, self.chemicals_list)

def check_file():
    try:
        with open("chemicals_list.txt", "r") as f:
            f.readlines()
    except FileNotFoundError:
        with open("chemicals_list.txt", "w") as f:
            f.write("SodiumChloride,58.44,SOLID")

def update_cb(cb, chemicals_list):
    cb.clear()
    cb.addItems([i.name for i in chemicals_list])

def update_chemical_list():
    with open("chemicals_list.txt", "r") as f:
        chemicals_list = [chemical(i.split(",")[0], i.split(",")[1], i.split(",")[2]) for i in f.readlines()]
    return chemicals_list


def is_number(string):
    try:
        print(string)
        float(string)
        return True
    except ValueError:
        return False

check_file()
concentration_calculator = QApplication([])
main_window = main_window()
main_window.show()
sys.exit(concentration_calculator.exec())
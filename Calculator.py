import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QSizePolicy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 400, 300)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout(centralWidget)  # Set layout to centralWidget

        # Initialize input fields
        self.inputField1 = QLineEdit()
        self.inputField2 = QLineEdit()
        self.setupValidators()

        # Set placeholders
        self.inputField1.setPlaceholderText("Enter first number: ")
        self.inputField2.setPlaceholderText("Enter second number: ")

        # Set size policy for input fields
        self.inputField1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.inputField2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Add input fields to layout
        layout.addWidget(self.inputField1)
        layout.addWidget(self.inputField2)

        # Initialize and style the output label
        self.label = QLabel("Output", alignment=Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 2px solid black; background-color: silver; padding: 5px; }")
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout.addWidget(self.label)

        # Dictionary mapping operations to lambda functions
        self.operations = {
            "Add": lambda a, b: a + b,
            "Subtract": lambda a, b: a - b,
            "Multiply": lambda a, b: a * b,
            "Divide": lambda a, b: "Error: Division by Zero" if b == 0 else a / b,
        }

        # Create buttons for each operation
        self.buttons = []
        for op_name, op_function in self.operations.items():
            button = QPushButton(op_name)
            button.clicked.connect(lambda _, fn=op_function: self.calculate(fn))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            layout.addWidget(button)
            self.buttons.append(button)  # Add button to the list

    def setupValidators(self):
        validator = QDoubleValidator()
        self.inputField1.setValidator(validator)
        self.inputField2.setValidator(validator)

    def calculate(self, operation):
        value1, value2 = self.inputField1.text(), self.inputField2.text()
        if not value1 or not value2:
            self.label.setText("Please enter valid numbers")
            return
        try:
            num1, num2 = float(value1), float(value2)
            result = operation(num1, num2)
            self.label.setText(f"{result}")
        except ValueError:
            self.label.setText("Invalid input")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resizeText()

    def resizeText(self):
        new_size = self.calculateFontSizeBasedOnWindowSize()
        font = self.inputField1.font()
        font.setPointSize(new_size)
        # Update font for all widgets
        self.inputField1.setFont(font)
        self.inputField2.setFont(font)
        self.label.setFont(font)
        for button in self.buttons:  # Iterate over buttons to update the font
            button.setFont(font)

    def calculateFontSizeBasedOnWindowSize(self):
        base_size = 10
        height_factor = self.height() * 0.01
        return base_size + height_factor

def main():
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()

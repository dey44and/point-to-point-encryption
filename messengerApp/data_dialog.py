from PyQt5.QtWidgets import (QLineEdit, QVBoxLayout, QDialog, QLabel, QPushButton)


class DataInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Your Data")
        layout = QVBoxLayout(self)
        layout.setSpacing(20)  # Increase spacing between widgets

        # Create labels and input fields
        self.name_label = QLabel("Name:")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        self.port_label = QLabel("Port:")
        layout.addWidget(self.port_label)
        self.port_input = QLineEdit()
        layout.addWidget(self.port_input)

        # Create OK button
        self.ok_button = QPushButton("OK")
        layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.accept)

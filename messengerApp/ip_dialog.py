from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox


class IPInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("IP and Port Input")

        layout = QVBoxLayout()

        # IP Address Input
        self.ip_label = QLabel("IP Address:")
        self.ip_input = QLineEdit()
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)

        # Port Input
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_ip_and_port(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        return ip, port

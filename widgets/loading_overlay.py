from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.hide()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)
        
        layout = QVBoxLayout()
        label = QLabel("Loading...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
    
    def showEvent(self, event):
        self.setGeometry(self.parent().rect())
        
    def paintEvent(self, event):
        self.setGeometry(self.parent().rect())
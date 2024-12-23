from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QStackedWidget)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from styles import STYLES

class AuthWindow(QWidget):
    login_success = pyqtSignal(str)  # Emit username on successful login

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Dextton Smart AI - Authentication')
        self.setStyleSheet(STYLES['main_window'])
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        
        # Login page
        login_widget = QWidget()
        login_layout = QVBoxLayout()
        
        logo_label = QLabel()
        logo_pixmap = QPixmap('c:/crypto/trading-bot/gui/src/Logo.svg')
        scaled_pixmap = logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        # logo_label.setSyleSheet({
        #     'margin-bottom': '20px',
        # })
        logo_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(logo_label)
        
        # Add spacing between logo and title
        login_layout.addSpacing(80)
        
        # # Login title
        # login_title = QLabel('Login')
        # login_title.setStyleSheet(STYLES['heading'])
        # login_title.setAlignment(Qt.AlignCenter)
        # login_layout.addWidget(login_title)
        
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText('Email')
        self.login_email.setStyleSheet(STYLES['input_field'])
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Password')
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setStyleSheet(STYLES['input_field'])
        
        login_button = QPushButton('Login')
        login_button.setStyleSheet(STYLES['primary_button'])
        login_button.clicked.connect(self.handle_login)
        
        switch_to_register = QPushButton("NOTE: Use your Dextton's credentials")
        switch_to_register.setStyleSheet(STYLES['link_button'])
        # switch_to_register.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        support_button = QPushButton('Get Support')
        support_button.setStyleSheet(STYLES['primary_button'])
        from PyQt5.QtGui import QDesktopServices
        from PyQt5.QtCore import QUrl
        support_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('mailto:info@dextton.com')))
        
        # login_layout.addWidget(login_title)
        login_layout.addWidget(self.login_email)
        login_layout.addWidget(self.login_password)
        login_layout.addWidget(login_button)
        login_layout.addWidget(switch_to_register)
        login_layout.addStretch()
        login_layout.addWidget(support_button)
        login_layout.setAlignment(support_button, Qt.AlignCenter)
        login_widget.setLayout(login_layout)
        
        # Register page
        # register_widget = QWidget()
        # register_layout = QVBoxLayout()
        
        # register_title = QLabel('Register')
        # register_title.setStyleSheet(STYLES['heading'])
        
        # self.register_name = QLineEdit()
        # self.register_name.setPlaceholderText('Full Name')
        # self.register_name.setStyleSheet(STYLES['input_field'])
        
        # self.register_email = QLineEdit()
        # self.register_email.setPlaceholderText('Email')
        # self.register_email.setStyleSheet(STYLES['input_field'])
        
        # self.register_password = QLineEdit()
        # self.register_password.setPlaceholderText('Password')
        # self.register_password.setEchoMode(QLineEdit.Password)
        # self.register_password.setStyleSheet(STYLES['input_field'])
        
        # register_button = QPushButton('Register')
        # register_button.setStyleSheet(STYLES['button'])
        # register_button.clicked.connect(self.handle_register)
        
        # switch_to_login = QPushButton('Already have an account? Login')
        # switch_to_login.setStyleSheet(STYLES['link_button'])
        # switch_to_login.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        # register_layout.addWidget(register_title)
        # register_layout.addWidget(self.register_name)
        # register_layout.addWidget(self.register_email)
        # register_layout.addWidget(self.register_password)
        # register_layout.addWidget(register_button)
        # register_layout.addWidget(switch_to_login)
        # register_layout.addStretch()
        # register_widget.setLayout(register_layout)
        
        self.stacked_widget.addWidget(login_widget)
        # self.stacked_widget.addWidget(register_widget)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def handle_login(self):
        # Add your login logic here
        # For demo, we'll just emit success
        if self.login_email.text() and self.login_password.text():
            self.login_success.emit(self.login_email.text())

    def handle_register(self):
        # Add your registration logic here
        # For demo, we'll just switch to login
        if all([self.register_name.text(), 
                self.register_email.text(), 
                self.register_password.text()]):
            self.stacked_widget.setCurrentIndex(0)
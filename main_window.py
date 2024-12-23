from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from pages import CombinedPage, SetupPage
from utils.api_client import APIClient
from utils.error_handler import show_error
from widgets.loading_overlay import LoadingOverlay
from styles import STYLES

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QTimer, Qt

class SupportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Loading message
        self.loading_label = QLabel("Opening Your Mail App...")
        self.loading_label.setStyleSheet("""
            QLabel {
                color: #7aa2f7;
                font-size: 16px;
                font-weight: bold;
                background-color: #1a1b26;
            }
        """)
        self.loading_label.setAlignment(Qt.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(self.loading_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def showEvent(self, event):
        super().showEvent(event)
        # Delay email launch by 1 second
        QTimer.singleShot(1000, self.launch_email)
        
    def launch_email(self):
        QDesktopServices.openUrl(QUrl('mailto:info@dextton.com'))
        # Return to dashboard after another second
        QTimer.singleShot(2000, lambda: self.parent().setCurrentIndex(0))

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        # self.api_client = APIClient()
        self.loading_overlay = LoadingOverlay(self)
        # self.update_timer = None
        self.init_ui()
        # self.setup_timer()

    def init_ui(self):
        self.setWindowTitle(f'Dextton Smart AI - {self.username}')
        self.setMinimumSize(1280, 720)
        self.setStyleSheet(STYLES['main_window'])
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Navigation bar
        nav_bar = QWidget()
        nav_bar_layout = QHBoxLayout(nav_bar)
        nav_bar_layout.setContentsMargins(15, 10, 15, 10)
        nav_bar_layout.setSpacing(10)
        nav_bar.setStyleSheet(STYLES['nav_bar'])

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('c:/crypto/trading-bot/gui/src/Logo.svg').scaled(300, 300, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        nav_bar_layout.addWidget(logo_label)

        # Heading
        # heading_label = QLabel("DEXTONN Trading Bot")
        # heading_label.setStyleSheet(STYLES['nav_heading'])
        # nav_bar_layout.addWidget(heading_label)

        # Spacer to push tabs to the left
        nav_bar_layout.addStretch()

        main_layout.addWidget(nav_bar)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(STYLES['tab_widget'])
        main_layout.addWidget(self.tabs)
        
        # Combined page
        self.combined_page = CombinedPage()
        self.tabs.addTab(self.combined_page, "Dashboard")
        
        # Setup page
        self.setup_page = SetupPage()
        self.tabs.addTab(self.setup_page, "Setup")

        self.support_page = SupportPage()
        self.tabs.addTab(self.support_page, "Get Support")


    # def setup_timer(self):
    #     self.update_timer = QTimer(self)
    #     self.update_timer.timeout.connect(self.update_data)
    #     self.update_timer.start(60000)  # Update every minute
    
    # def update_data(self):
    #     try:
    #         self.loading_overlay.show()
    #         # Fetch data from API client
    #         account_data = self.api_client.get_account_data()
    #         positions = self.api_client.get_positions()
    #         order = self.api_client.get_current_order()
    #         # Update combined page with fetched data
    #         self.combined_page.update_data(account_data, positions, order)
    #     except Exception as e:
    #         show_error(self, "Error", f"Failed to update data: {str(e)}")
    #     finally:
    #         self.loading_overlay.hide()
    
    # def closeEvent(self, event):
    #     if self.update_timer:
    #         self.update_timer.stop()
    #     event.accept()

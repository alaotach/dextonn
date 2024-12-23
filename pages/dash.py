from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QGroupBox, QPushButton, QFrame, QGridLayout, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from styles import STYLES
import subprocess
import sys
import os
import atexit
import psutil

# Import your new dashboard_data utility
from utils.dashboard_data import get_dashboard_data

from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon

class AccountSummaryWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['group_box'])
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        icon_label = QLabel()
        icon_pixmap = QPixmap('assets/account_icon.png').scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        title_label = QLabel("Account Summary")
        title_label.setStyleSheet(STYLES['group_title'])

        # Add refresh button
        refresh_button = QToolButton()
        refresh_button.setIcon(QIcon('assets/refresh_icon.png'))
        refresh_button.clicked.connect(self.refresh_data)

        header_layout = QHBoxLayout()
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(refresh_button)  # Add refresh button to header

        layout.addLayout(header_layout, 0, 0, 1, 2)

        self.balance_label = QLabel('Total Balance:')
        self.balance_label.setStyleSheet(STYLES['label'])
        self.balance_value = QLabel('$0.00')
        self.balance_value.setStyleSheet(STYLES['value_label'])

        self.equity_label = QLabel('Equity:')
        self.equity_label.setStyleSheet(STYLES['label'])
        self.equity_value = QLabel('$0.00')
        self.equity_value.setStyleSheet(STYLES['value_label'])

        self.margin_label = QLabel('Available Margin:')
        self.margin_label.setStyleSheet(STYLES['label'])
        self.margin_value = QLabel('$0.00')
        self.margin_value.setStyleSheet(STYLES['value_label'])

        layout.addWidget(self.balance_label, 1, 0)
        layout.addWidget(self.balance_value, 1, 1)
        layout.addWidget(self.equity_label, 2, 0)
        layout.addWidget(self.equity_value, 2, 1)
        layout.addWidget(self.margin_label, 3, 0)
        layout.addWidget(self.margin_value, 3, 1)

        self.setLayout(layout)
        
    def update_summary(self, balance, equity, margin):
        self.balance_value.setText(f'${balance:,.2f}')
        self.equity_value.setText(f'${equity:,.2f}')
        self.margin_value.setText(f'${margin:,.2f}')

    def refresh_data(self):
        # Emit a signal to refresh data
        self.parent().auto_refresh_data()

class CombinedPage(QWidget):
    def __init__(self):
        super().__init__()
        self.bot_process = None  # Store the subprocess reference
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_refresh_data)
        self.timer.start(10_000)  # 10 seconds

        # Ensure subprocess is terminated on exit
        atexit.register(self.cleanup_subprocess)

    def run_bot(self):
        try:
            if self.bot_process is None:
                
                base_dir = os.path.dirname(__file__)

                bot_path = os.path.join(base_dir[:-6], 'bot.py')
                ps_command = f'Start-Process -NoNewWindow python -ArgumentList "{bot_path}"'
                
                self.bot_process = subprocess.Popen(
                    ['powershell.exe', '-Command', ps_command],
                    shell=True,
                    cwd=base_dir[:-6]
                )
                
                self.run_bot_btn.setEnabled(False)
                self.run_bot_btn.setText("Bot Running...")
                self.stop_bot_btn.setEnabled(True)
                print(f"Bot started with PID: {self.bot_process.pid}")
        except Exception as e:
            print(f"Error starting bot: {e}")

    def stop_bot(self):
        if self.bot_process is not None:
            try:
                print(f"Stopping bot with PID: {self.bot_process.pid}")
                self.terminate_process_tree(self.bot_process.pid)
                self.bot_process = None
                self.run_bot_btn.setEnabled(True)
                self.run_bot_btn.setText("Run Bot")
                self.stop_bot_btn.setEnabled(False)
            except Exception as e:
                print(f"Error stopping bot: {e}")

    def terminate_process_tree(self, pid):
        try:
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                print(f"Terminating child process PID: {child.pid}")
                child.terminate()
            parent.terminate()
            parent.wait(5)  # Wait up to 5 seconds for termination
            print(f"Bot process {pid} terminated successfully.")
        except psutil.NoSuchProcess:
            print(f"Process {pid} does not exist.")
        except psutil.AccessDenied:
            print(f"Access denied when trying to terminate process {pid}.")
        except psutil.TimeoutExpired:
            print(f"Process {pid} did not terminate in time; forcing kill.")
            parent.kill()

    def cleanup_subprocess(self):
        if self.bot_process is not None:
            print("Cleaning up subprocess...")
            self.terminate_process_tree(self.bot_process.pid)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Account Summary Section
        self.summary_widget = AccountSummaryWidget()
        main_layout.addWidget(self.summary_widget)

        # Positions and Orders Section
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(20)

        # Positions Table
        self.positions_table = PositionsTable()
        positions_group = QGroupBox()
        positions_group.setStyleSheet(STYLES['group_box'])
        positions_layout = QVBoxLayout()
        positions_layout.setSpacing(10)
        positions_layout.addWidget(self.positions_table)
        positions_group.setLayout(positions_layout)

        # Orders Table
        self.orders_table = OrdersTable()
        orders_group = QGroupBox()
        orders_group.setStyleSheet(STYLES['group_box'])
        orders_layout = QVBoxLayout()
        orders_layout.setSpacing(10)
        orders_layout.addWidget(self.orders_table)
        orders_group.setLayout(orders_layout)

        tables_layout.addWidget(positions_group)
        tables_layout.addWidget(orders_group)

        main_layout.addLayout(tables_layout)

        # Run and Stop Bot Buttons
        buttons_layout = QHBoxLayout()
        self.run_bot_btn = QPushButton("Run Bot")
        self.run_bot_btn.setStyleSheet(STYLES['primary_button'])
        self.run_bot_btn.clicked.connect(self.run_bot)

        self.stop_bot_btn = QPushButton("Stop Bot")
        self.stop_bot_btn.setStyleSheet(STYLES['secondary_button'])
        self.stop_bot_btn.clicked.connect(self.stop_bot)
        self.stop_bot_btn.setEnabled(False)

        buttons_layout.addWidget(self.run_bot_btn)
        buttons_layout.addWidget(self.stop_bot_btn)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def auto_refresh_data(self):
        """
        Called by QTimer every 10 seconds.
        Fetches the latest data from the external file and updates the UI.
        """
        account_data, positions, orders = get_dashboard_data()
        self.update_data(account_data, positions, orders)

    def update_data(self, account_data, positions, orders):
        self.summary_widget.update_summary(
            account_data.get('balance', 0),
            account_data.get('equity', 0),
            account_data.get('available_margin', 0)
        )
        self.positions_table.update_positions(positions)
        self.orders_table.update_orders(orders)

class PositionsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['table'])
        self.init_ui()

    def calculate_column_width(self):
        table_width = self.width()
        return int((table_width / 485) * 95)  # 95:1200 ratio

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.calculate_column_width()
        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            self.setColumnWidth(i, width)
            header.setSectionResizeMode(i, QHeaderView.Fixed)

    def init_ui(self):
        headers = ['Symbol', 'Size', 'Entry Price', 'Current Price', 'PnL']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setVisible(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setAlternatingRowColors(True)

    def update_positions(self, positions):
        self.setRowCount(len(positions))
        for row, pos in enumerate(positions):
            self.setItem(row, 0, QTableWidgetItem(pos.get('symbol', '')))
            self.setItem(row, 1, QTableWidgetItem(str(pos.get('size', 0))))
            self.setItem(row, 2, QTableWidgetItem(pos.get('entry_price', 0)))
            self.setItem(row, 3, QTableWidgetItem(pos.get('current_price', 0)))
            pnl = (pos.get('pnl', 0))
            pnl_item = QTableWidgetItem((pnl))
            pnl_item.setForeground(Qt.green if float(pnl) >= 0 else Qt.red)
            self.setItem(row, 4, pnl_item)

class OrdersTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['table'])
        self.init_ui()

    def calculate_column_width(self):
        table_width = self.width()
        return int((table_width / 485) * 79)  # 79:1200 ratio

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.calculate_column_width()
        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            self.setColumnWidth(i, width)
            header.setSectionResizeMode(i, QHeaderView.Fixed)

    def init_ui(self):
        headers = ['Symbol', 'Type', 'Side', 'Price', 'Amount', 'Status']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setVisible(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setAlternatingRowColors(True)

    def update_orders(self, orders):
        self.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.setItem(row, 0, QTableWidgetItem(order.get('symbol', '')))
            self.setItem(row, 1, QTableWidgetItem(order.get('type', '')))
            self.setItem(row, 2, QTableWidgetItem(order.get('side', '')))
            self.setItem(row, 3, QTableWidgetItem(order.get('price', 0)))
            self.setItem(row, 4, QTableWidgetItem(str(order.get('amount', 0))))
            self.setItem(row, 5, QTableWidgetItem(order.get('status', '')))
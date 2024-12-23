from PyQt5.QtWidgets import QMessageBox

def show_error(parent, title, message):
    QMessageBox.critical(parent, title, message)

def show_warning(parent, title, message):
    QMessageBox.warning(parent, title, message)

def show_info(parent, title, message):
    QMessageBox.information(parent, title, message)
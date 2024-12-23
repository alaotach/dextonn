# FILE: trading-bot/gui/src/styles.py

STYLES = {
    'main_window': """
        QWidget {
            background-color: #1a1b26;
            color: #c0caf5;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """,

    'page_title': """
        QLabel {
            color: #FFFFFF;
            font-size: 28px;
            font-weight: bold;
            padding: 20px 0;
            margin-bottom: 20px;
        }
    """,

    'input_field': """
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #3A3A3A;
            border-radius: 5px;
            color: #E0E0E0;
            padding: 10px 15px;
            margin: 5px 0;
        }
        QLineEdit:focus {
            border: 1px solid #7aa2f7;
        }
        QLineEdit::placeholder {
            color: #808080;
        }
    """,

    'button': """
        QPushButton {
            background-color: #FF6F61;
            color: #FFFFFF;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            font-size: 14px;
            margin: 10px 0;
        }
        QPushButton:hover {
            background-color: #FF847C;
        }
        QPushButton:pressed {
            background-color: #E85A4F;
        }
    """,

    'link_button': """
        QPushButton {
            background: transparent;
            border: none;
            color: #c9261a;
            text-decoration: underline;
            font-size: 14px;
            font-weight: bold;
            margin: 5px
        }
        QPushButton:hover {
            color: #c9261a;
        }
        QPushButton:pressed {
            color: #c9261a;
        }
    """,

    'heading': """
        QLabel {
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        }
    """,

    'label': """
        QLabel {
            color: #a9b1d6;
            font-size: 14px;
            font-weight: bold;
        }
    """,

    'group_box': """
        QGroupBox {
            border: 1px solid #414868;
            border-radius: 12px;
            margin-top: 15px;
        }
        QGroupBox::title {
            color: #7aa2f7;
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px;
            font-weight: bold;
        }
    """,

    'text_area': """
        QTextEdit {
            background-color: #1E1E1E;
            border: 1px solid #3A3A3A;
            border-radius: 5px;
            color: #E0E0E0;
            padding: 10px;
            font-family: 'Consolas', monospace;
            font-size: 13px;
        }
    """,

    'slider': """
        QSlider::groove:horizontal {
            border: 1px solid #3A3A3A;
            height: 8px;
            background: #1E1E1E;
            margin: 2px 0;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #50fa7b;
            border: 1px solid #1E1E1E;
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #FF847C;
        }
    """,

    'tab_widget': """
        QTabWidget::pane {
            border: 1px solid #3A3A3A;
            background: #1E1E1E;
            border-radius: 5px;
            margin-top: -1px;
        }
        QTabBar::tab {
            background: #1E1E1E;
            color: #E0E0E0;
            padding: 10px 20px;
            border: 1px solid #3A3A3A;
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            min-width: 100px;
            margin-right: 5px;
        }
        QTabBar::tab:selected {
            background: #FF6F61;
            color: #FFFFFF;
            font-weight: bold;
        }
        QTabBar::tab:hover:!selected {
            background: #3A3A3A;
        }
    """,

        'table': """
        QTableWidget {
            background-color: #1a1b26;
            color: #c0caf5;
            gridline-color: #414868;
            border: none;
            border-radius: 8px;
            padding: 5px;
        }
        QHeaderView::section {
            background-color: #24283b;
            color: #7aa2f7;
            padding: 12px 16px;
            border: none;
            font-weight: bold;
            font-size: 14px;
            border-right: 1px solid #414868;
        }
        QHeaderView::section:last {
            border-right: none;
        }
        QTableWidget::item {
            padding: 12px 16px;
            border: none;
            border-bottom: 1px solid #414868;
            background: transparent;
            font-size: 13px;
        }
        QTableWidget::item:alternate {
            background-color: #1f2335;
        }
        QTableWidget::item:selected {
            background-color: #364A82;
            color: #c0caf5;
            border-radius: 4px;
        }
        QTableWidget::item:hover {
            background-color: #2c324c;
            border-radius: 4px;
        }
    """,

    'progress_bar': """
        QProgressBar {
            background-color: #1E1E1E;
            border: 1px solid #3A3A3A;
            border-radius: 5px;
            text-align: center;
            color: #E0E0E0;
        }
        QProgressBar::chunk {
            background-color: #FF6F61;
            border-radius: 5px;
        }
    """,
    'value_label': """
        QLabel {
            color: #7aa2f7;
            font-size: 16px;
            font-weight: bold;
            margin-left: 15px;
        }
    """,
    'primary_button': """
        QPushButton {
            background-color: #7aa2f7;
            color: #1a1b26;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #89b4fa;
        }
        QPushButton:pressed {
            background-color: #6b91e6;
            padding: 14px 24px 10px 24px;
        }
    """,
    'secondary_button': """
        QPushButton {
            background-color: #24283b;
            color: #7aa2f7;
            padding: 12px 24px;
            border: 1.5px solid #7aa2f7;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #2c324c;
            border-color: #89b4fa;
        }
        QPushButton:pressed {
            background-color: #1a1b26;
            padding: 14px 24px 10px 24px;
        }
    """,
    'nav_bar': """
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #24283b, stop:1 #1a1b26);
            border-bottom: 2px solid #7aa2f7;
            padding: 10px;
        }
    """,
    'nav_heading': """
        QLabel {
            color: #7aa2f7;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 1px;
        }
    """,
    'group_title': """
        QLabel {
            color: #7aa2f7;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
    """,
    'cta_button': """
        QPushButton {
            background-color: #7aa2f7;
            color: #1a1b26;
            border: none;
            border-radius: 4px;
            padding: 5px 20px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #89b4ff;
        }
        QPushButton:pressed {
            background-color: #6992e7;
        }
    """,
        'input_field_setup': """
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #3A3A3A;
            border-radius: 5px;
            color: #E0E0E0;
            padding: 20px 10px;
            margin: 5px 0;
        }
        QLineEdit:focus {
            border: 1px solid #7aa2f7;
        }
        QLineEdit::placeholder {
            color: #808080;
        }
    """,
}
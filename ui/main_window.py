from scanner.windows_registry import get_installed_apps
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UpdateChecker Pro")
        self.resize(900, 600)

        # مرکزی
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # عنوان
        title = QLabel("UpdateChecker Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            padding: 10px;
        """)
        layout.addWidget(title)

        # جدول
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["App", "Installed", "Latest"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # دکمه
        self.scan_btn = QPushButton("Scan Apps")
        self.scan_btn.setStyleSheet("""
            padding: 10px;
            background-color: #2b2d31;
            color: white;
            border-radius: 8px;
        """)

        self.scan_btn.clicked.connect(self.scan_apps)
        layout.addWidget(self.scan_btn)

        # استایل کلی
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1f22;
            }

            QTableWidget {
                background-color: #2b2d31;
                color: white;
            }

            QPushButton:hover {
                background-color: #40434a;
            }
        """)

    def scan_apps(self):
        try:
            apps = get_installed_apps() or []
        except Exception as e:
            # show error in single-row table
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Error"))
            self.table.setItem(0, 1, QTableWidgetItem(str(e)))
            self.table.setItem(0, 2, QTableWidgetItem("-"))
            return

        # ensure apps is an iterable of (name, version)
        try:
            items = list(apps)
        except TypeError:
            items = []

        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            try:
                name, version = item
            except Exception:
                name = str(item)
                version = ""

            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(version))
            self.table.setItem(row, 2, QTableWidgetItem("Checking..."))
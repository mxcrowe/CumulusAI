"""Main application window for CumulusAI."""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        self.setWindowTitle("CumulusAI - Weather Station")
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Placeholder content
        label = QLabel("CumulusAI - Coming Soon!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; padding: 20px;")
        layout.addWidget(label)

        status_label = QLabel("Application Status: Initializing...")
        status_label.setStyleSheet("color: gray; padding: 10px;")
        layout.addWidget(status_label)

        # Setup menu bar
        self.setup_menu_bar()

        # Setup status bar
        self.statusBar().showMessage("Ready")

    def setup_menu_bar(self):
        """Setup the application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Dashboard")
        view_menu.addAction("Graphs")
        view_menu.addAction("Records")

        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings")
        tools_menu.addAction("Import Data")
        tools_menu.addAction("Export Data")

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About")
        help_menu.addAction("Documentation")

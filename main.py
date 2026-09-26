import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QGroupBox, QPushButton, QDialog, QDialogButtonBox, QLineEdit, QFileDialog, QHBoxLayout, QInputDialog
from backupMan import loadFile, createCategory, createFile

dir = os.path.expanduser("~/.local/share/shiori")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shiori")
        self.setGeometry(0, 1000, 400, 400)

        mainContainer = QWidget()
        self.setCentralWidget(mainContainer)
        self.mainLayout = QVBoxLayout()
        mainContainer.setLayout(self.mainLayout)
        self.loadCategories()

    def loadCategories(self):
        directory = os.listdir(dir)
        for category in directory:
            groupBox = QGroupBox()
            categoryLayout = QVBoxLayout()

            header = QHBoxLayout()
            title = QLabel(category)
            backupButton = QPushButton("+")
            backupButton.clicked.connect(
                lambda checked, category=category: self.addBackup(category)
            )
            backupButton.setFixedWidth(30)
            header.addWidget(title)
            header.addStretch()
            header.addWidget(backupButton)

            categoryLayout.addLayout(header)

            for backup in os.listdir(os.path.join(dir, category)):
                if backup == "index.json" : continue
                button = QPushButton(backup)
                button.clicked.connect(
                    lambda checked, category=category, backup=backup:
                        loadFile(category, backup)
                )
                categoryLayout.addWidget(button)

            groupBox.setLayout(categoryLayout)
            self.mainLayout.addWidget(groupBox)
        buttonAdd = QPushButton("Add Category")
        buttonAdd.clicked.connect(self.addCategory)
        self.mainLayout.addWidget(buttonAdd)

    def addCategory(self):
        dialog = newCategory()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            category = dialog.categoryName.text()
            path = dialog.filePath.text()
            createCategory(category, path)
            self.refreshCategories()

    def addBackup(self, category):
        name, yes = QInputDialog.getText(
            self,
            "Create backup",
            "Backup name:"
        )
        if name and yes:
            createFile(category, name)
            self.refreshCategories()

    def refreshCategories(self):
        while self.mainLayout.count():
            item = self.mainLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.loadCategories()

class newCategory(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new category")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Category name:"))
        self.categoryName = QLineEdit()
        self.categoryName.setPlaceholderText("e.g. Picom")
        layout.addWidget(self.categoryName)
        layout.addWidget(QLabel("File path:"))

        pathLayout = QHBoxLayout()
        self.filePath = QLineEdit()
        self.filePath.setPlaceholderText("Path to file")
        pathLayout.addWidget(self.filePath)
        browseButton = QPushButton("Browse")
        browseButton.clicked.connect(self.browse)
        pathLayout.addWidget(browseButton)
        layout.addLayout(pathLayout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file"
        )
        if path:
            self.filePath.setText(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

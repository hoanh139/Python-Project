from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea, QApplication, QMainWindow, QLineEdit, \
    QHBoxLayout, QListWidget, QMenu, QStatusBar, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIcon
import os
import sys

class CustomScrollArea(QScrollArea):
    imageClicked = pyqtSignal(str)

    def mousePressEvent(self, event):
        item = self.childAt(event.pos())
        if item and hasattr(item, 'text'):
            image_name = item.text()
            self.imageClicked.emit(image_name)
            print(image_name)
        super().mousePressEvent(event)

class ClickableLabel(QWidget):
    def __init__(self, text, image_path, on_click):
        super().__init__()

        # QLabel for text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)

        # QLabel for image
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

        # Layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.setFixedWidth(pixmap.width())

        # Save text for later use
        self.text = text

        # Connect the signal to the slot (method)
        self.clicked = on_click

        # Set the cursor to indicate that the widget is clickable
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked(self.text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main layout
        main_layout = QHBoxLayout()

        # Left side layout
        left_layout = QVBoxLayout()

        # Input fields for patient ID and Gewichtung
        self.inputField(left_layout)

        # Scrollable area for patient pictures
        self.scrollArena()

        # Update the left side scrollable area based on input
        self.update_scroll_area()

        # self.scroll_area.setWidget(self.scroll_widget)
        left_layout.addWidget(self.scroll_area)

        self.scroll_area.imageClicked.connect(self.update_selected_picture)

        # Middle layout for displaying the chosen picture
        middle_layout = QVBoxLayout()
        self.displayChosenPicture(middle_layout)

        # Right layout with buttons
        right_layout = QVBoxLayout()
        self.rightButtonMenu(right_layout)

        # Add the three layouts to the main layout
        main_layout.addLayout(left_layout, 35)
        main_layout.addLayout(middle_layout, 60)
        main_layout.addLayout(right_layout, 5)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create menu bar
        self.menu()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Connect input field signals to update scroll area
        self.patient_id_input.textChanged.connect(self.update_scroll_area)
        self.gewichtung_input.textChanged.connect(self.update_scroll_area)

        # Set default values for patient ID and Gewichtung
        self.patient_id_input.setText('220030')
        self.gewichtung_input.setText('42')

        # Initialize the status bar with default values
        self.update_status_bar(1)

        # Set window properties
        self.setWindowTitle('Patient Information')
        self.setGeometry(100, 100, 800, 500)


    def inputField(self, left_layout):
        self.patient_id_label = QLabel('Patient ID:')
        self.patient_id_input = QLineEdit()
        self.gewichtung_label = QLabel('Gewichtung:')
        self.gewichtung_input = QLineEdit()

        left_layout.addWidget(self.patient_id_label)
        left_layout.addWidget(self.patient_id_input)
        left_layout.addWidget(self.gewichtung_label)
        left_layout.addWidget(self.gewichtung_input)

    def scrollArena(self):
        self.scroll_area = CustomScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

    def displayChosenPicture(self, middle_layout):
        self.picture_label = QLabel('Selected Picture')
        pixmap = QPixmap('./data/220030/Gewichtung_42/01.jpeg')
        self.picture_label.setPixmap(pixmap)

        # Adjust the size to make the image a little bigger
        scaled_pixmap = pixmap.scaledToWidth(300)  # Adjust the width as needed
        self.picture_label.setPixmap(scaled_pixmap)

        # Center the image in the QLabel
        self.picture_label.setAlignment(Qt.AlignCenter)

        middle_layout.addWidget(self.picture_label)

    def rightButtonMenu(self, right_layout):
        button_list = QListWidget()
        button_list.addItem(QListWidgetItem(QIcon('picture/pencil-2-64.png'), ''))
        button_list.addItem(QListWidgetItem(QIcon('picture/scissors-7-64.png'), ''))
        button_list.addItem(QListWidgetItem(QIcon('picture/trash-6-64.png'), ''))
        button_list.addItem(QListWidgetItem(QIcon('picture/undo-2-64.png'), ''))
        button_list.addItem(QListWidgetItem(QIcon('picture/redo-2-64.png'), ''))
        button_list.addItem(QListWidgetItem(QIcon('picture/question-mark-4-64.png'), ''))

        button_list.setFixedWidth(30)

        right_layout.addWidget(button_list)


    def menu(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = QMenu('&Datei', self)
        edit_menu = QMenu('&Edit', self)
        navigation_menu = QMenu('&Navigation', self)
        help_menu = QMenu('&Hilfe', self)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(navigation_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)
    def update_selected_picture(self, image_name):
        # Update the selected picture based on the clicked item in the scroll area
        patient_id = self.patient_id_input.text()
        gewichtung = "Gewichtung_" + self.gewichtung_input.text()
        image_path = f'./data/{patient_id}/{gewichtung}/{image_name}'
        pixmap = QPixmap(image_path)
        self.picture_label.setPixmap(pixmap)

        # Adjust the size to make the image a little bigger
        scaled_pixmap = pixmap.scaledToWidth(300)  # Adjust the width as needed
        self.picture_label.setPixmap(scaled_pixmap)

        # Center the image in the QLabel
        self.picture_label.setAlignment(Qt.AlignCenter)

        self.update_status_bar(image_name)

        print(image_path)

    def update_status_bar(self, selected_item):
        # Update status bar with current patient information
        patient_id = self.patient_id_input.text()
        gewichtung = "Gewichtung_" + self.gewichtung_input.text()
        status_text = f'Patient ID: {patient_id} | Gewichtung: {gewichtung} | Current Picture: {selected_item}'
        self.status_bar.showMessage(status_text)

    def update_scroll_area(self):
        # Update the left side scrollable area based on input
        patient_id = self.patient_id_input.text()
        gewichtung = "Gewichtung_" + self.gewichtung_input.text()

        # Clear existing items
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # Load pictures based on the provided directory structure
        picture_path = f'./data/{patient_id}/{gewichtung}' if patient_id and gewichtung else ''
        if os.path.exists(picture_path):
            picture_files = [f for f in os.listdir(picture_path) if f.lower().endswith('.jpeg')]
            for file_name in sorted(picture_files):
                picture_widget = ClickableLabel(file_name, os.path.join(picture_path, file_name), self.update_selected_picture)
                self.scroll_layout.addWidget(picture_widget)
                self.scroll_area.setFixedWidth(picture_widget.width()+25)

        # Update the scroll area widget
        self.scroll_area.setWidget(self.scroll_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

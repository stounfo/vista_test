import webbrowser
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from db_methods import Database
from utils import reverse_status


class Editor(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("54"))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


class New_note(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        layout = self.update_editor()

        add_note_button = QPushButton("Add note")
        add_note_button.clicked.connect(self.add_note)
        layout.addWidget(add_note_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_note(self):
        database.insert_into_wishlist(name=self.name_text,
                                      cost=int(self.cost_text),
                                      url=self.url_text,
                                      description=self.description_text)
        self.close()

    def update_name_text(self):
        self.name_text = self.name.text()

    def update_cost_text(self):
        self.cost_text = self.cost.value()

    def update_url_text(self):
        self.url_text = self.url.text()

    def update_description_text(self):
        self.description_text = self.description.text()

    def update_editor(self):
        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        self.name.textChanged.connect(self.update_name_text)
        layout.addWidget(self.name)

        self.cost = QSpinBox()
        self.cost.setMinimum(0)
        self.cost.setMaximum(100500)
        self.cost.setValue(0)
        self.cost.valueChanged.connect(self.update_cost_text)
        layout.addWidget(self.cost)

        self.url = QLineEdit()
        self.url.setPlaceholderText("URL")
        self.url.textChanged.connect(self.update_url_text)
        layout.addWidget(self.url)

        self.description = QLineEdit()
        self.description.setPlaceholderText("Description")
        self.description.textChanged.connect(self.update_description_text)
        layout.addWidget(self.description)

        return layout


class Wishlist(QMainWindow):
    editors = list()

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Wishlist")

        self.update_menu("Active")

    def open_webbrowser(self, url):
        webbrowser.open(url)

    def open_new_note(self):
        self.new_note = New_note()
        self.new_note.show()
    
    def open_edit(self):
        window = Editor()
        window.show()
        self.editors.append(window)

    def change_status(self, note_id, status):
        database.change_note_status(note_id, status)
        self.update_menu(reverse_status(status))


    def update_menu(self, status):
        layout = QHBoxLayout()

        active_button = QPushButton("Active")
        active_button.clicked.connect(partial(self.update_menu, "Active"))
        layout.addWidget(active_button)

        done_button = QPushButton("Done")
        done_button.clicked.connect(partial(self.update_menu, "Done"))
        layout.addWidget(done_button)

        new_note_button = QPushButton("New note")
        new_note_button.clicked.connect(self.open_new_note)
        layout.addWidget(new_note_button)

        main_menu = QWidget()
        main_menu.setLayout(layout)

        layout = QVBoxLayout()
        for note in database.select_from_wishlist([status]):
            one_note = QWidget()
            note_layout = QHBoxLayout()
            note_layout.addWidget(QLabel(str(note["name"])))
            note_layout.addWidget(QLabel(str(note["cost"])))
            note_layout.addWidget(QLabel(str(note["description"])))
            
            url_button = QPushButton("URL")
            url_button.clicked.connect(partial(self.open_webbrowser, note["url"]))
            note_layout.addWidget(url_button)

            if status == "Active":
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(self.open_edit)
                note_layout.addWidget(edit_button)
            else:
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(partial(self.change_status, note["note_id"], "Deleted"))
                note_layout.addWidget(remove_button)

            done_button = QPushButton(f"Add to {reverse_status(status).lower()}")
            done_button.clicked.connect(partial(self.change_status, 
                                                note["note_id"],
                                                reverse_status(status)))
            note_layout.addWidget(done_button)

            one_note.setLayout(note_layout)
            layout.addWidget(one_note)
        
        notes_menu = QWidget()
        notes_menu.setLayout(layout)
        
        layout = QVBoxLayout()
        layout.addWidget(main_menu)
        layout.addWidget(notes_menu)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        



if __name__ == '__main__':
    database = Database(db_type="mysql+pymysql",
            name="root",
            password="asd",
            host="localhost",
            port="3306",
            database="wishlist")

    app = QApplication([])
    window = Wishlist()
    window.show()
    app.exec_()

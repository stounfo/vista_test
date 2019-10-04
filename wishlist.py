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

        layout = QHBoxLayout()
        layout.addWidget(QLabel("54"))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


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

        #=====================

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
            done_button.clicked.connect(partial(self.change_status, note["note_id"], reverse_status(status)))
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

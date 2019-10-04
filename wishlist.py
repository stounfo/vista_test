import webbrowser
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from db_methods import Database
from utils import reverse_status



class Alert(QMainWindow):
    def __init__(self):
       QMainWindow.__init__(self)
       self.setCentralWidget(QLabel("Some lines is empty"))


class New_note(QMainWindow):
    def __init__(self, main_window):
        QMainWindow.__init__(self)
        self.main_window = main_window

        layout = self.update_editor()

        add_note_button = QPushButton("Add note")
        add_note_button.clicked.connect(self.add_note)
        layout.addWidget(add_note_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_note(self):
        if (self.name_text is None or self.url_text is None or self.description_text is None):
            self.window = Alert()
            self.window.show()
        else:
            database.insert_into_wishlist(name=self.name_text,
                                      cost=int(self.cost_text),
                                      url=self.url_text,
                                      description=self.description_text)
            self.main_window.update_menu("Active")
            self.close()
            
    def update_name_text(self):
        self.name_text = self.name.text()

    def update_cost_text(self):
        self.cost_text = self.cost.value()

    def update_url_text(self):
        self.url_text = self.url.text()

    def update_description_text(self):
        self.description_text = self.description.text()

    def update_editor(self, name=None, cost=0, url=None, description=None):
        layout = QVBoxLayout()

        self.name_text = name
        self.cost_text = cost
        self.url_text = url
        self.description_text = description


        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        self.name.setText(self.name_text)
        self.name.textChanged.connect(self.update_name_text)
        layout.addWidget(self.name)

        self.cost = QSpinBox()
        self.cost.setMinimum(0)
        self.cost.setMaximum(100500)
        self.cost.setValue(self.cost_text)
        self.cost.valueChanged.connect(self.update_cost_text)
        layout.addWidget(self.cost)

        self.url = QLineEdit()
        self.url.setPlaceholderText("URL")
        self.url.setText(self.url_text)
        self.url.textChanged.connect(self.update_url_text)
        layout.addWidget(self.url)

        self.description = QLineEdit()
        self.description.setPlaceholderText("Description")
        self.description.setText(self.description_text)
        self.description.textChanged.connect(self.update_description_text)
        layout.addWidget(self.description)

        return layout


class Editor(New_note):
    def __init__(self, note_id, main_window):
        QMainWindow.__init__(self)
        self.main_window = main_window
        self.note_id = note_id

        note_data = database.get_note_data(note_id)

        layout = self.update_editor(name=note_data["name"],
                                    cost=note_data["cost"],
                                    url=note_data["url"],
                                    description=note_data["description"])

        add_note_button = QPushButton("Update note")
        add_note_button.clicked.connect(self.update_note)
        layout.addWidget(add_note_button)
        
        info = QLabel(f'Create: {note_data["tms_create"]} Update: {note_data["tms_update"]}')
        layout.addWidget(info)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_note(self):
        if (self.name_text is None or self.url_text is None or self.description_text is None):
            self.window = Alert()
            self.window.show()
        else:
            database.update_wishlist(note_id=self.note_id,
                                    name=self.name_text,
                                    cost=int(self.cost_text),
                                    url=self.url_text,
                                    description=self.description_text)
            self.main_window.update_menu("Active")
            self.close()


class Wishlist(QMainWindow):
    editors = list()

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Wishlist")

        self.update_menu("Active")

    def open_webbrowser(self, url):
        webbrowser.open(url)

    def open_new_note(self):
        self.new_note = New_note(self)
        self.new_note.show()
    
    def open_edit(self, note_id):
        window = Editor(note_id, self)
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
                edit_button.clicked.connect(partial(self.open_edit, note["note_id"]))
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

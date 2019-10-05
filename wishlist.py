import webbrowser
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from db_methods import Database
from utils import create_h_widget, create_v_widget


class Button(QPushButton):
    def __init__(self, text, func, *args):
        QPushButton.__init__(self, text)
        self.clicked.connect(partial(func, *args))


class Alert(QMainWindow):
    def __init__(self, text):
       QMainWindow.__init__(self)
       self.setCentralWidget(create_v_widget(QLabel(text), Button("Ok", self._close_window)))

    def _close_window(self):
        self.close()


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
            self.window = Alert("Some lines are empty")
            self.window.show()
        else:
            database.insert_into_wishlist(name=self.name_text,
                                      cost=int(self.cost_text),
                                      url=self.url_text,
                                      description=self.description_text)
            main_window.render_active_notes()
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


class Main_window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.navbar_widget = self.render_navbar()
        self.render_active_notes()

    def render_navbar(self):
        active_button = Button("Active", self.render_active_notes)
        done_button = Button("Done", self.render_done_notes)
        new_note_button = Button("New note", self._create_note)
        return create_h_widget(active_button, done_button, new_note_button)
    
    def render_active_notes(self):
        notes_data = self._get_notes_data("Active")
        if notes_data == []:
            self.setCentralWidget(create_v_widget(self.navbar_widget, 
                                                        QLabel("There are no notes active")))
            return None

        layout = QVBoxLayout()
        for note in notes_data:
            name_label = QLabel(note["name"])
            cost_label = QLabel(str(note["cost"]))
            description_label = QLabel(note["description"])

            url_button = Button("URL", self._open_url_in_webbrowser, note["url"])
            edit_button = Button("Edit", self._edit_note, note["note_id"])
            add_to_done_button = Button("Done", self._change_note_status, note["note_id"], "Done")

            layout.addWidget(create_h_widget(name_label, cost_label, description_label, 
                                                    url_button, edit_button, add_to_done_button))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(create_v_widget(self.navbar_widget, widget))

    def render_done_notes(self):
        notes_data = self._get_notes_data("Done")
        
        if notes_data == []:
            self.setCentralWidget(create_v_widget(self.navbar_widget, QLabel("There are no notes done")))
            return None

        layout = QVBoxLayout()
        for note in notes_data:
            name_label = QLabel(note["name"])
            cost_label = QLabel(str(note["cost"]))
            description_label = QLabel(note["description"])

            url_button = Button("URL", self._open_url_in_webbrowser, note["url"])
            remove_button = Button("Remove", self._change_note_status, note["note_id"], "Deleted")
            add_to_done_button = Button("Add to active", self._change_note_status, note["note_id"], "Active")

            layout.addWidget(create_h_widget(name_label, cost_label, description_label, 
                                                    url_button, remove_button, add_to_done_button))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(create_v_widget(self.navbar_widget, widget))

    def _create_note(self):
        self.new_note = New_note(self)
        self.new_note.show()

    def _edit_note(self, note_id):
        print(note_id)

    def _change_note_status(self, note_id, status):
        database.change_note_status(note_id, status)
        if status == "Done":
            self.render_active_notes()
        elif status == "Active":
            self.render_done_notes()
        elif status == "Deleted":
            self.render_done_notes()

    def _get_notes_data(self, status):
        return database.select_from_wishlist([status])
    
    def _open_url_in_webbrowser(self, url):
        webbrowser.open(url)        



if __name__ == '__main__':
    database = Database(db_type="mysql+pymysql",
            name="root",
            password="asd",
            host="localhost",
            port="3306",
            database="wishlist")

    app = QApplication([])
    main_window = Main_window()
    main_window.show()
    app.exec_()

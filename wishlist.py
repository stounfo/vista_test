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


class LineEdit(QLineEdit):
    def __init__(self, placeholder_text, text):
        QLineEdit.__init__(self)
        self.setPlaceholderText(placeholder_text)
        self.setText(text)


class SpinBox(QSpinBox):
    def __init__(self, value, minimum, maximum):
        QSpinBox.__init__(self)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)


class Alert(QMainWindow):
    def __init__(self, text):
       QMainWindow.__init__(self)
       self.setCentralWidget(create_v_widget(QLabel(text), Button("Ok", self._close_window)))

    def _close_window(self):
        self.close()


class New_note(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self._render()
    
    def _render(self, name=None, cost=0, url=None, description=None):
        self.name = LineEdit("Name", name)
        self.cost = SpinBox(cost, 0, 100500)
        self.url = LineEdit("url", url)
        self.description = LineEdit("Description", description)
        button = Button("Add", self._button_func)
        self.setCentralWidget(create_v_widget(self.name, self.cost, self.url, self.description, button))

    def _button_func(self):
        if self.name.text() == "" or self.url.text() == "" or self.description.text() == "":
            self.alert = Alert("Some lines are empty")
            self.alert.show()
        else:
            self._add_note(self.name.text(), self.cost.value(), self.url.text(), self.description.text())
            main_window.render_active_notes()
            self.close()

    def _add_note(self, name, cost, url, description):
        database.insert_into_wishlist(name=name, cost=cost, url=url, description=description)


class Editor(New_note):
    def __init__(self, note_id, name, cost, url, description):
        QMainWindow.__init__(self)
        self.note_id = note_id
        print(note_id)
        self._render(name, cost, url, description)

    def _button_func(self):
        if self.name.text() == "" or self.url.text() == "" or self.description.text() == "":
            self.alert = Alert("Some lines are empty")
            self.alert.show()
        else:
            self._update_note()
            main_window.render_active_notes()
            self.close()
    
    def _update_note(self):
        database.update_wishlist(self.note_id, self.name.text(), self.cost.value(), self.url.text(), self.description.text())


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
            edit_button = Button("Edit", self._edit_note, note["note_id"],
                                        note["name"], note["cost"], note["url"], note["description"])
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
        self.new_note = New_note()
        self.new_note.show()

    def _edit_note(self, note_id, name, cost, url, description):
        self.edit_note = Editor(note_id, name, cost, url, description)
        self.edit_note.show()

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
            name="wishlist",
            password="wishlist",
            host="localhost",
            port="3306",
            database="wishlist")

    app = QApplication([])
    main_window = Main_window()
    main_window.show()
    app.exec_()

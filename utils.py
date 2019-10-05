from datetime import datetime
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

def datetime_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_h_widget(*args):
    layout = QHBoxLayout()
    for widget in args:
        layout.addWidget(widget)
    widget = QWidget()
    widget.setLayout(layout)
    return widget

def create_v_widget(*args):
    layout = QVBoxLayout()
    for widget in args:
        layout.addWidget(widget)
    widget = QWidget()
    widget.setLayout(layout)
    return widget

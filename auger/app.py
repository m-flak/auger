# pylint: disable=no-name-in-module
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow

def get_app_instance():
    instance = QCoreApplication.instance()

    if instance is None:
        raise RuntimeError('No instance could be found!')
    if 'AugerApplication' not in instance.__class__.__name__:
        raise RuntimeError('Instance is not AugerApplication!')

    return instance

class AugerApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._main_window = None

    @property
    def main_window(self):
        return self._main_window

    @main_window.setter
    def main_window(self, value):
        if not isinstance(value, QMainWindow):
            raise TypeError('main_window must be a QMainWindow!')

        self._main_window = value

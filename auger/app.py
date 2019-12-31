# pylint: disable=no-name-in-module
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow
from .ocr import AugerOCR
from .commands import AugerCommandManager

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
        self._ocr = None
        self._settings = None
        self._cmd_mgr = None

    @property
    def main_window(self):
        return self._main_window

    @main_window.setter
    def main_window(self, value):
        if not isinstance(value, QMainWindow):
            raise TypeError('main_window must be a QMainWindow!')

        self._main_window = value

    @property
    def ocr(self):
        if self._ocr is None:
            self._ocr = AugerOCR(self)
        return self._ocr

    @property
    def settings(self):
        if self._settings is None:
            self._settings = QSettings('m-flak', 'auger', self)
        return self._settings

    @property
    def cmd_mgr(self):
        if self._cmd_mgr is None:
            self._cmd_mgr = AugerCommandManager(self)
        return self._cmd_mgr

    def __del__(self):
        # deleting a QSettings in pyqt saves the settings
        del self._settings

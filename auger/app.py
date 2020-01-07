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
        self._documents = dict(image=None, text=None)

        self.setApplicationName('auger')

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
            self._settings = QSettings('m-flak', self.applicationName(), self)
        return self._settings

    @property
    def cmd_mgr(self):
        if self._cmd_mgr is None:
            self._cmd_mgr = AugerCommandManager(self)
        return self._cmd_mgr

    @property
    def image_document(self):
        return self._documents.get('image', None)

    @image_document.setter
    def image_document(self, value):
        if self._documents.get('image', None) is None:
            self._documents['image'] = value

    @property
    def text_document(self):
        return self._documents.get('text', None)

    @text_document.setter
    def text_document(self, value):
        if self._documents.get('text', None) is None:
            self._documents['text'] = value

    def __del__(self):
        # deleting a QSettings in pyqt saves the settings
        del self._settings

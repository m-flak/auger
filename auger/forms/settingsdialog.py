# pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from ..app import get_app_instance
from .resource import Resource, Resources, Ui

class SettingsDialog(QDialog):
    sig_backendless = pyqtSignal()

    def __init__(self, parent=None, flags=Qt.WindowFlags(Qt.Dialog)):
        super().__init__(parent, flags)
        # window modality is set within the ui file

        self._chosen_backend = ''

        uic.loadUi(Resources().resource(Resource.ResourceUi, which=Ui.UiSettingsDlg),
                   self)

        # connect signals
        self.sig_backendless.connect(self.slot_no_backend)
        self.comboOCRBackend.currentIndexChanged.connect(self.slot_ocr_changed)

        # remap slots to our slot naming conventions
        self.accept = lambda s=self.slot_accept: s()
        self.open = lambda s=self.slot_open: s()

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_accept(self):
        get_app_instance().ocr.tool = self._chosen_backend
        get_app_instance().settings.setValue('chosen_tool', self._chosen_backend)
        return super().accept()

    def slot_open(self):
        # Populate the OCR Backend combo box
        if get_app_instance().ocr.tools:
            self.comboOCRBackend.addItems(get_app_instance().ocr.tools.keys())
        else:
            self.sig_backendless.emit()

        # if this isn't None, then the tool was found in the settings file
        if get_app_instance().ocr.tool is not None:
            # make sure its a choice b4 doing anything further
            t_idx = self.comboOCRBackend.findText(
                get_app_instance().ocr.tool.get_name(),
                Qt.MatchFixedString
            )
            if t_idx != -1:
                self.comboOCRBackend.setCurrentIndex(t_idx)

        return super().open()

    def slot_no_backend(self):
        QMessageBox.critical(
            self,
            'There are no OCR backends installed!',
            'Auger was unable to find an OCR backend.\nPlease install an OCR backend such as Tesseract.',
            QMessageBox.Ok,
            QMessageBox.Ok
        )

    def slot_ocr_changed(self, current):
        self._chosen_backend = self.comboOCRBackend.itemText(current)

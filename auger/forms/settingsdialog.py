# pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import Qt, QVariant, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from ..app import get_app_instance
from .resource import Resource, Resources, Ui

class SettingsDialog(QDialog):
    sig_backendless = pyqtSignal()
    sig_nolanguage = pyqtSignal()

    def __init__(self, parent=None, flags=Qt.WindowFlags(Qt.Dialog)):
        super().__init__(parent, flags)
        # window modality is set within the ui file

        self._chosen_backend = ''
        self._default_lang = ''

        uic.loadUi(Resources().resource(Resource.ResourceUi, which=Ui.UiSettingsDlg),
                   self)

        # connect signals
        self.sig_backendless.connect(self.slot_no_backend)
        self.sig_nolanguage.connect(self.slot_no_language)
        self.comboOCRBackend.currentIndexChanged.connect(self.slot_ocr_changed)
        self.comboOCRDefaultLang.currentIndexChanged.connect(self.slot_lang_changed)

        # remap slots to our slot naming conventions
        self.accept = lambda s=self.slot_accept: s()
        self.open = lambda s=self.slot_open: s()

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_accept(self):
        get_app_instance().ocr.tool = self._chosen_backend
        get_app_instance().settings.setValue('chosen_tool', self._chosen_backend)
        get_app_instance().ocr.default_language = self._default_lang
        get_app_instance().settings.setValue('default_language', self._default_lang)

        return super().accept()

    def slot_open(self):
        # Populate the OCR Backend combo box
        if get_app_instance().ocr.tools:
            self.comboOCRBackend.addItems(get_app_instance().ocr.tools.keys())
        else:
            self.sig_backendless.emit()
            return super().open()

        # Match the control to what's in the settings
        if get_app_instance().ocr.tool is not None:
            # make sure its a choice b4 doing anything further
            t_idx = self.comboOCRBackend.findText(
                get_app_instance().ocr.tool.get_name(),
                Qt.MatchFixedString
            )
            if t_idx != -1:
                self.comboOCRBackend.setCurrentIndex(t_idx)

        # Populate the OCR default language combo box
        if get_app_instance().ocr.languages:
            for lang_name, lang_code in get_app_instance().ocr.languages.items():
                self.comboOCRDefaultLang.addItem(
                    lang_name,
                    QVariant(lang_code)
                )
        else:
            self.sig_nolanguage.emit()
            return super().open()

        # Match the control to what's in the settings
        if get_app_instance().ocr.default_language is not None:
            l_idx = self.comboOCRDefaultLang.findData(
                QVariant(get_app_instance().ocr.default_language)
            )
            if l_idx != -1:
                self.comboOCRDefaultLang.setCurrentIndex(l_idx)

        return super().open()

    def slot_no_backend(self):
        QMessageBox.critical(
            self,
            'There are no OCR backends installed!',
            'Auger was unable to find an OCR backend.\nPlease install an OCR backend such as Tesseract.',
            QMessageBox.Ok,
            QMessageBox.Ok
        )

    def slot_no_language(self):
        QMessageBox.critical(
            self,
            'No valid language can be found for OCR!',
            'Auger was unable to determine which language to default to.\nPlease fix your system locales.',
            QMessageBox.Ok,
            QMessageBox.Ok
        )

    def slot_ocr_changed(self, current):
        self._chosen_backend = self.comboOCRBackend.itemText(current)

    def slot_lang_changed(self, current):
        self._default_lang = self.comboOCRDefaultLang.itemText(current)

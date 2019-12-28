# pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from .resource import Resource, Resources, Ui
import auger

class AboutDialog(QDialog):
    def __init__(self, parent=None, flags=Qt.WindowFlags(Qt.Dialog)):
        super().__init__(parent, flags)
        # window modality is set within the ui file

        self._auger_icon = QPixmap()
        self._auger_icon.load(Resources().resource(Resource.ResourceIcon), None)

        uic.loadUi(
            Resources().resource(
                Resource.ResourceUi,
                which=Ui.UiAboutDlg
            ),
            self
        )

        self.labelAugerIcon.setPixmap(self._auger_icon)
        with_version = ''.join([self.labelAugerNameVersion.text(), auger.__version__])
        self.labelAugerNameVersion.setText(with_version)

        self.buttonBox.clicked.connect(self.slot_close_clicked)

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_close_clicked(self):
        self.accept()

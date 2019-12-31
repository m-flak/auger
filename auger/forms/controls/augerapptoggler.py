# pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from ..resource import Resource, Resources, ToolIcon

class AugerAppendToggler(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setCheckable(True)
        self.setFlat(True)

        self.setAccessibleName('toolbutton')

        self.icon_checked = QIcon(
            Resources().resource(Resource.ResourceToolIcon, which=ToolIcon.ToolIconAppendOn)
        )
        self.icon_unchecked = QIcon(
            Resources().resource(Resource.ResourceToolIcon, which=ToolIcon.ToolIconAppendOff)
        )

        self.tip_checked = 'Append Output. (Keeps Changes)'
        self.tip_unchecked = 'Overwrite Output. (Discards Changes)'

        # DEFAULT STATE IS UNCHECKED
        # so set the icon
        self.setIcon(self.icon_unchecked)

        self.clicked.connect(self.slot_click)

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_click(self):
        if self.isChecked():
            self.setIcon(self.icon_checked)
            self.setToolTip(self.tip_checked)
        else:
            self.setIcon(self.icon_unchecked)
            self.setToolTip(self.tip_unchecked)

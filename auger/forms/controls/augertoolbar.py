# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QFontComboBox, QLabel, QLineEdit, QPushButton
)
from ...app import get_app_instance
from ..resource import Resource, Resources, ToolIcon
from .augerapptoggler import AugerAppendToggler

class AugerToolbar(QWidget):
    sig_font_changed = pyqtSignal(str)
    sig_size_changed = pyqtSignal(int)
    sig_ao_toggle = pyqtSignal(bool)

    def __init__(self, parent, flags=Qt.WindowFlags(Qt.Widget)):
        super().__init__(parent, flags)

        font_size_tooltip = 'Font Size (in pt.)'
        ao_tooltip = 'Append / Overwrite (Default: Overwrite)'

        # Font Selector
        self._fontbox = QFontComboBox(self)
        self._fontbox.currentFontChanged.connect(self.slot_font_changed)

        # Font Size Label Hint
        self._label_size = QLabel(self)
        self._label_size_pixmap = QPixmap()
        self._label_size_pixmap.load(
            Resources().resource(Resource.ResourceToolIcon,
                                 which=ToolIcon.ToolIconFontSize),
            None
        )
        self._label_size.setFixedSize(25, 25)
        self._label_size.setPixmap(self._label_size_pixmap)
        self._label_size.setToolTip(font_size_tooltip)

        # Font Size Input
        self._fontsize = QLineEdit('8', self)
        self._fontsize.setMaxLength(3)
        self._fontsize.setInputMask('00D')
        self._fontsize.setFixedSize(36, self._fontbox.height())
        self._fontsize.setToolTip(font_size_tooltip)
        self._fontsize.textChanged.connect(self.slot_size_changed)

        # The Append / Overwrite Toggler
        self._appendtoggler = AugerAppendToggler(self)
        self._appendtoggler.setFixedSize(25, 25)
        self._appendtoggler.setToolTip(ao_tooltip)
        self._appendtoggler.clicked.connect(self.slot_append_toggle)

        # The Undo Button
        self._undobutton = QPushButton(self)
        self._undobutton.setFixedSize(25, 25)
        self._undobutton.setToolTip('Undo')
        self._undobutton.setAccessibleName('toolbutton')
        self._undobutton.setIcon(
            QIcon(
                Resources().resource(Resource.ResourceToolIcon,
                                     which=ToolIcon.ToolIconUndo)
            )
        )
        self._undobutton.setFlat(True)
        self._undobutton.setEnabled(False)
        self._undobutton.clicked.connect(self.slot_undo_clicked)

        # The Redo Button
        self._redobutton = QPushButton(self)
        self._redobutton.setFixedSize(25, 25)
        self._redobutton.setToolTip('Redo')
        self._redobutton.setAccessibleName('toolbutton')
        self._redobutton.setIcon(
            QIcon(
                Resources().resource(Resource.ResourceToolIcon,
                                     which=ToolIcon.ToolIconRedo)
            )
        )
        self._redobutton.setFlat(True)
        self._redobutton.setEnabled(False)
        self._redobutton.clicked.connect(self.slot_redo_clicked)

        # The Layout holding all toolbar contents
        self._layout = QHBoxLayout(self)
        self._layout.addWidget(self._fontbox)
        self._layout.addWidget(self._label_size)
        self._layout.addWidget(self._fontsize)
        self._layout.addWidget(self._appendtoggler)
        self._layout.addWidget(self._undobutton)
        self._layout.addWidget(self._redobutton)

        self.setLayout(self._layout)

        # connect slots to the command manager for undo / redo
        get_app_instance().cmd_mgr.sig_undo_stack_changed.connect(self.slot_undo_available)
        get_app_instance().cmd_mgr.sig_redo_stack_changed.connect(self.slot_redo_available)

    # Override method
    def paintEvent(self, paint_event): # pylint: disable=invalid-name
        def border_coords():
            coords = paint_event.rect()
            return coords.x(), coords.y(), coords.width(), coords.height()
        #
        # # # # # # # # # # #
        # make coordinates for border
        draw_rect = tuple(map(
            lambda x, y: x+y,
            border_coords(),
            (1, 1, -2, -2)
        ))

        # Prevent the painting of a border around children within the widget
        if not self.childrenRect().contains(paint_event.rect()):
            painter = QPainter(self)
            painter.setPen(QPen(QColor(130, 135, 144, 255)))
            painter.drawRect(*draw_rect)

        return super().paintEvent(paint_event)

    def set_font_properties(self, family, size):
        self._fontbox.setCurrentFont(QFont(family))
        self._fontsize.setText(str(size))

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_font_changed(self, font):
        self.sig_font_changed.emit(font.family())

    def slot_size_changed(self, str_size):
        try:
            font_size = int(str_size)
        except ValueError:
            font_size = 0

        if font_size > 0:
            self.sig_size_changed.emit(font_size)

    def slot_append_toggle(self, state):
        self.sig_ao_toggle.emit(state)

    def slot_undo_available(self, num_undos):
        if num_undos > 0:
            self._undobutton.setEnabled(True)
        else:
            self._undobutton.setEnabled(False)

    def slot_redo_available(self, num_redos):
        if num_redos > 0:
            self._redobutton.setEnabled(True)
        else:
            self._redobutton.setEnabled(False)

    def slot_undo_clicked(self): # pylint: disable=no-self-use
        get_app_instance().cmd_mgr.undo_last_command()

    def slot_redo_clicked(self): # pylint: disable=no-self-use
        get_app_instance().cmd_mgr.redo_last_command()

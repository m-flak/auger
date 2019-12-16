# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QFont
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QFontComboBox, QLabel, QLineEdit
)
from ..resource import Resource, Resources, ToolIcon

class AugerToolbar(QWidget):
    sig_font_changed = pyqtSignal(str)
    sig_size_changed = pyqtSignal(int)

    def __init__(self, parent, flags=Qt.WindowFlags(Qt.Widget)):
        super().__init__(parent, flags)

        font_size_tooltip = 'Font Size (in pt.)'

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

        # The Layout holding all toolbar contents
        self._layout = QHBoxLayout(self)
        self._layout.addWidget(self._fontbox)
        self._layout.addWidget(self._label_size)
        self._layout.addWidget(self._fontsize)

        self.setLayout(self._layout)

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

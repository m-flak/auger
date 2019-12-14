# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem
from ...app import get_app_instance

class AugerView(QGraphicsView):
    sig_select_start = pyqtSignal(tuple)
    sig_select_end = pyqtSignal(tuple, tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For toggling the selection on & off
        self._select_toggle = False
        # Coordinates of selection start & end
        self._select_start_coords = tuple()
        self._select_end_coords = tuple()

        # the rectangle for selection
        self._rectangle_selection = None

    def _map_select_start_coords(self):
        start_coords = self._select_start_coords
        qpt_sc = self.mapToScene(*start_coords).toPoint()
        self._select_start_coords = (qpt_sc.x(), qpt_sc.y())

    def _map_select_end_coords(self):
        end_coords = self._select_end_coords
        qpt_ec = self.mapToScene(*end_coords).toPoint()
        self._select_end_coords = (qpt_ec.x(), qpt_ec.y())

    @property
    def select_toggle(self):
        return self._select_toggle

    @select_toggle.setter
    def select_toggle(self, value):
        self._select_toggle = value

    # Override method
    def mousePressEvent(self, mouse_event): # pylint: disable=invalid-name
        # toggle selection state
        self.select_toggle = not self.select_toggle

        # Emit signal with coords
        if self.select_toggle:
            self._select_start_coords = (mouse_event.x(), mouse_event.y())
            self._map_select_start_coords()
            self.sig_select_start.emit(self._select_start_coords)
        else:
            self._select_end_coords = (mouse_event.x(), mouse_event.y())
            self._map_select_end_coords()
            self.sig_select_end.emit(
                self._select_start_coords,
                self._select_end_coords
            )

        auger_mw = get_app_instance().main_window

        if auger_mw.property('imageHasBeenLoaded') is True:
            # A selection already exists when starting a new selection
            if self._rectangle_selection is not None and self.select_toggle:
                rectangle = list(filter(
                    lambda i: isinstance(i, QGraphicsRectItem),
                    self.scene().items()
                ))
                try:
                    self.scene().removeItem(*rectangle)
                except TypeError:
                    self._rectangle_selection = None
                self._rectangle_selection = None
            # A selection already exists when ending a current selection
            elif self._rectangle_selection is not None and not self.select_toggle:
                rectangle = list(filter(
                    lambda i: isinstance(i, QGraphicsRectItem),
                    self.scene().items()
                ))
                # resize the rectangle to reflect user's selection
                rectangle[0].setRect(
                    self._select_start_coords[0],
                    self._select_start_coords[1],
                    self._select_end_coords[0]-self._select_start_coords[0],
                    self._select_end_coords[1]-self._select_start_coords[1]
                )

            # Create a new selection
            if self._rectangle_selection is None:
                pixmap = list(filter(
                    lambda i: isinstance(i, QGraphicsPixmapItem),
                    self.scene().items()
                ))
                self._rectangle_selection = QGraphicsRectItem(
                    self._select_start_coords[0],
                    self._select_start_coords[1],
                    50,
                    50,
                    *pixmap
                )
                self._rectangle_selection.setBrush(QBrush(Qt.green, Qt.Dense4Pattern))
                self._rectangle_selection.setPen(QPen(QColor(Qt.darkGreen)))

        return super().mousePressEvent(mouse_event)

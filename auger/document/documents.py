from abc import abstractmethod
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene

class DocumentInterface:
    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def contents(self):
        pass

    @property
    @abstractmethod
    def raw(self):
        pass

    @abstractmethod
    def load_document(self, load_callback):
        pass

    @abstractmethod
    def reset_document(self):
        pass

class RawContents:
    def __new__(cls, *args, **kwargs):
        inst = super(RawContents, cls).__new__(cls)
        for k, v in kwargs.items():
            setattr(inst, k, v)
        return inst

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, type_raw):
        return self.__dict__.get(type_raw, None)

class ImageDocument(DocumentInterface):
    def __init__(self, associated_view):
        super().__init__()

        self._selection = tuple()
        self._assoc_view = associated_view
        self._scene = QGraphicsScene(associated_view)
        self._pixmap = QPixmap()

    @property
    def contents(self):
        return self._scene

    @property
    def raw(self):
        raw_contents = RawContents(image=self._pixmap.toImage())
        return raw_contents('image')

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value):
        self._selection = tuple(value)

    @property
    def has_selection(self):
        # the same as an `if not ...` / etc.
        return bool(self._selection)

    @property
    def associated_view(self):
        return self._assoc_view

    def load_document(self, load_callback):
        load_callback(self._pixmap)

        if self._pixmap.isNull():
            return False

        self._scene.addPixmap(self._pixmap)
        self._scene.setSceneRect(
            0,
            0,
            self._pixmap.width(),
            self._pixmap.height()
        )

        return True

    def reset_document(self):
        self._scene.clear()

    def get_selection_as_image(self):
        if not self.has_selection:
            raise ValueError("No Selection.")

        return self._pixmap.toImage().copy(*self._selection)

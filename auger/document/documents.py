from abc import abstractmethod
from PyQt5.QtGui import QPixmap, QTextDocument
from PyQt5.QtWidgets import QGraphicsScene

class DocumentInterface:
    """ Interface for the documents that are loaded into Auger for editing.
    """
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

    @abstractmethod
    def save_document(self, file_obj, format):
        pass

class RawContents:
    """Convenience callable for representing the raw contents of a document.
    Keyword arguments become class members & can be accessed via __call__(name)
    """
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

    def save_document(self, file_obj, format):
        raise NotImplementedError

    def get_selection_as_image(self):
        if not self.has_selection:
            raise ValueError("No Selection.")

        return self._pixmap.toImage().copy(*self._selection)

class TextDocument(DocumentInterface):
    def __init__(self, *args, **kwargs):
        super(TextDocument, self).__init__(*args, **kwargs)

        self._raw_type = 'text'
        self._qtextdoc = QTextDocument(None)

    @property
    def contents(self):
        return self._qtextdoc

    @property
    def raw_type(self):
        return self._raw_type

    @raw_type.setter
    def raw_type(self, value):
        new_value = str(value)
        if new_value not in ('text', 'html'):
            raise ValueError('raw_type must equal \'text\' or \'html\'!')
        self._raw_type = value

    @property
    def raw(self):
        raw_contents = RawContents(
            text=self._qtextdoc.toPlainText(),
            html=self._qtextdoc.toHtml()
        )
        return raw_contents(self._raw_type)

    @staticmethod
    def get_raw_text(text_document):
        def do_get(text_doc, old_rt):
            text_doc.raw_type = 'text'
            rv = text_doc.raw
            text_doc.raw_type = old_rt
            return rv
        # # #
        if text_document is not None and isinstance(text_document, TextDocument):
            return do_get(text_document, text_document.raw_type)

        return ''

    @staticmethod
    def get_raw_html(text_document):
        def do_get(text_doc, old_rt):
            text_doc.raw_type = 'html'
            rv = text_doc.raw
            text_doc.raw_type = old_rt
            return rv
        # # #
        if text_document is not None and isinstance(text_document, TextDocument):
            return do_get(text_document, text_document.raw_type)

        return ''

    def load_document(self, load_callback):
        return

    def reset_document(self):
        self._qtextdoc.clear()

    def save_document(self, file_obj, format):
        fmt_method = {
            'text': TextDocument.get_raw_text,
            'html': TextDocument.get_raw_html
        }

        try:
            content_method = lambda m=fmt_method[format]: m(self)
            file_obj.write(content_method())
        except KeyError:
            print('Unable to save document. Invalid format.')

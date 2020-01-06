# pylint: disable=no-name-in-module
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit
import lxml.html
from ...app import get_app_instance

class BodyStyle:
    def __init__(self, font_family, font_size):
        self.font_family = font_family
        self.font_size = font_size

    def __repr__(self):
        return 'font-family:\'{}\'; font-size:{}pt;'.\
               format(self.font_family, self.font_size)

class InternalHTML:
    def __init__(self, html=None):
        self._html = html
        self._document = lxml.html.fromstring(html) if html else None

    @property
    def html(self):
        """The initial HTML code used to build `document`.
        """
        return self._html

    @html.setter
    def html(self, value):
        """The initial HTML code used to build `document`
        If this was not set in the constructor, it must be set before accessing
        `document`.
        """
        self._html = value

    @property
    def fresh_html(self):
        """The 'fresh' HTML code of `document`.
        """
        return lxml.html.tostring(self._document, method='html', encoding='unicode')

    @property
    def document(self):
        """An lxml document of the HTML code.
        NOTE!!!: The html property should be set BEFORE accessing this property.
        It can be set via either the constructor or `html`.
        """
        if self._document is None:
            if self._html is not None:
                self._document = lxml.html.fromstring(self._html)
        return self._document

    def __eq__(self, other):
        equals = (
            other.html == self.html,
            other.document == self.document #fresh_html is proven by this
        )
        return all(equals)

    def apply_body_style(self, body_style):
        body_style = str(body_style)
        self.document.body.set('style', body_style)

class AugerTextEdit(QTextEdit):
    sig_style_changed = pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._our_html = InternalHTML()
        self._font_family = QFont().defaultFamily()
        self._font_size = 8

        # remap slots to our slot naming conventions
        # pylint: disable=invalid-name
        self.setFontFamily = lambda a, s=self.slot_set_fontfamily: s(a)
        self.setFontPointSize = lambda a, s=self.slot_set_fontsize: s(a)

        self.sig_style_changed.connect(self.slot_style_changed)

        self.textChanged.connect(self.slot_text_changed)

    # Override method
    def setHtml(self, text): # pylint: disable=invalid-name
        new_html = InternalHTML(text)
        if self._our_html != new_html:
            self._our_html = new_html

        return super().setHtml(self._our_html.fresh_html)

    # Override method
    def toHtml(self): # pylint: disable=invalid-name
        if self._our_html.html is None or self._our_html.document is None:
            return super().toHtml()

        return self._our_html.fresh_html

    def transfer_text_to_other_html(self, other):
        if not isinstance(other, AugerTextEdit):
            raise TypeError

        other.setHtml(self.toPlainText())

    def transfer_html_to_other_text(self, other):
        if not isinstance(other, AugerTextEdit):
            raise TypeError

        other.setPlainText(self.toHtml())

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_set_fontfamily(self, family):
        super().setFontFamily(family)
        self._font_family = family
        self.sig_style_changed.emit((family, self._font_size))

    def slot_set_fontsize(self, size):
        super().setFontPointSize(size)
        self._font_size = size
        self.sig_style_changed.emit((self._font_family, size))

    def slot_style_changed(self, styles):
        if self._our_html.html is None or self._our_html.document is None:
            return

        self._our_html.apply_body_style(BodyStyle(*styles))
        self.setHtml(self._our_html.fresh_html)

    def slot_text_changed(self):
        try:
            if 'text' in self.property('augerTextEditType'):
                get_app_instance().text_document.contents.setHtml(self.toHtml())
            elif 'html' in self.property('augerTextEditType'):
                get_app_instance().text_document.contents.setHtml(self.toPlainText())
            else:
                return
        except:
            return

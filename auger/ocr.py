# pylint: disable=no-name-in-module
from io import BytesIO
from PyQt5.QtCore import QObject, QLocale, pyqtSignal
from PIL import Image
import pyocr
import pyocr.builders
import iso_language_codes as lingo

class ImageAdapter:
    """Callable that adapts a QImage into a PIL Image by directly reading the
    QImage's raw pixels into a PIL image object suitable for pyocr.
    """
    def __init__(self, qt_image):
        raw = qt_image.bits()
        # set the size of the region of memory at the bits pointer
        raw.setsize(qt_image.bytesPerLine()*qt_image.height())
        # Read raw RGBA pixels from QImage
        self._raw_image = BytesIO(raw)
        self._img_size = (qt_image.width(), qt_image.height())
        self._image = None

    def __call__(self):
        if self._image is None:
            self._image = Image.frombytes(
                'RGBA',
                self._img_size,
                self._raw_image.getvalue()
            )
        return self._image

class AugerOCR(QObject):
    sig_performed = pyqtSignal(str)
    sig_change_lang = pyqtSignal(str)
    sig_ocr_error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._tools = dict()
        self._languages = dict()
        self._tool_key = ''
        self._default_lang_key = ''
        self._use_lang_key = ''

    def setup_tools(self):
        tools = pyocr.get_available_tools()

        if not tools:
            return

        self._tools = {tool.get_name(): tool for tool in tools}

        # set the default tool to use
        # the user can change this later
        if not self._tool_key:
            self._tool_key = tools[0].get_name()

    def setup_languages(self):
        # get keys for language_dictionary from backend supported languages
        # fuck tesseract's language codes, but they wont stop us!
        def backend_to_lingo(lin_lang, be_lang, lang_dict):
            bel_len = 0
            for lingo_key in lin_lang:
                if bel_len > len(be_lang):
                    break
                for backend_lang in be_lang:
                    if lingo_key:
                        # tesseract uses codes based off of the name not ISO codes
                        language_name = lang_dict[lingo_key].get('Name').lower()
                        if backend_lang.startswith(lingo_key) or language_name.startswith(backend_lang):
                            bel_len += 1
                            yield lingo_key
        # # # # # # # # #
        try:
            backend_languages = self.tool.get_available_languages()
            lingo_languages = lingo.language_dictionary()
        except AttributeError:
            # There's no OCR backend. :/
            return

        # remove fake 'osd' language if it exists
        if 'osd' in backend_languages:
            backend_languages.remove('osd')

        # Get language names
        ldk = list(backend_to_lingo(lingo_languages.keys(), backend_languages, lingo_languages))
        language_names = [lingo_languages.get(l).get('Name') for l in ldk]

        # sort
        backend_languages = sorted(backend_languages)
        language_names = sorted(language_names)

        self._languages = {name: code for name, code in zip(language_names, backend_languages)}

        # set the default language to use & current language to use
        # the user can change these later
        # we'll pick the system default
        sys_lang = lingo.language(QLocale.system().name()[0:2]).get('Name')
        assert sys_lang in language_names
        self._use_lang_key = self._default_lang_key = sys_lang

    @property
    def tools(self):
        if not self._tools:
            self.setup_tools()
        return self._tools

    @property
    def languages(self):
        if not self._languages:
            self.setup_languages()
        return self._languages

    @property
    def tool(self):
        """Getter returns a pyocr tool object.
        """
        try:
            return self.tools[self._tool_key]
        except KeyError:
            return None

    @tool.setter
    def tool(self, value):
        """Setter expects string, corresponding to a key in the _tools dict.
        """
        self._tool_key = value

    @property
    def default_language(self):
        """Getter returns a string appropriate for pyocr function arguments.
        """
        try:
            return self.languages[self._default_lang_key]
        except KeyError:
            return None

    @default_language.setter
    def default_language(self, value):
        """Setter expects a formal language name string, a key of _languages.
        """
        self._default_lang_key = value

    @property
    def use_language(self):
        """Getter returns a string appropriate for pyocr function arguments.
        """
        try:
            return self.languages[self._use_lang_key]
        except KeyError:
            return None

    @use_language.setter
    def use_language(self, value):
        """Setter expects a formal language name string, a key of _languages.
        """
        self._use_lang_key = value

    def perform_ocr(self, qt_image):
        image = ImageAdapter(qt_image)

        try:
            # Attempt OCR with 'Use' language
            text = self.tool.image_to_string(
                image(),
                lang=self.use_language,
                builder=pyocr.builders.TextBuilder()
                )

                # Use the default / fallback language if the above operation yielded
                # no results
            if not text:
                text = self.tool.image_to_string(
                    image(),
                    lang=self.default_language,
                    builder=pyocr.builders.TextBuilder()
                )

        except Exception as e:
            self.sig_ocr_error.emit(str(e))
            return

        self.sig_performed.emit(text)

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_change_use_lang(self, new_lang):
        self.use_language = new_lang
        self.sig_change_lang.emit(new_lang)

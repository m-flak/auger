# pylint: disable=no-name-in-module
from io import BytesIO
from PyQt5.QtCore import QObject, pyqtSignal
from PIL import Image
import pyocr
import pyocr.builders

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

    def __init__(self, parent=None):
        super().__init__(parent)

        self._tools = dict()
        self._tool_key = ''

    def setup_tools(self):
        tools = pyocr.get_available_tools()

        if not tools:
            return

        self._tools = {tool.get_name(): tool for tool in tools}

    @property
    def tools(self):
        if not self._tools:
            self.setup_tools()
        return self._tools

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

    def perform_ocr(self, qt_image):
        image = ImageAdapter(qt_image)
        #TODO: Add multiple language support
        text = self.tool.image_to_string(
            image(),
            lang='eng',
            builder=pyocr.builders.TextBuilder()
        )

        self.sig_performed.emit(text)

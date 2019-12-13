# pylint: disable=no-name-in-module
from PyQt5.QtCore import QObject
import pyocr

class AugerOCR(QObject):
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

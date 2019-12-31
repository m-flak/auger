# pylint: disable=no-name-in-module
# pylint: disable=len-as-condition
import collections.abc
from PyQt5.QtCore import QObject

class CommandStack(collections.abc.Collection):
    def __init__(self):
        self._parent = QObject(None)
        self._index = 0
        self._command_number = 1

    def __len__(self):
        return len(self._parent.children())

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if len(self) == 0:
            raise StopIteration

        if self._index < len(self):
            self._index += 1
            return self._parent.children()[self._index-1]

        raise StopIteration

    def __contains__(self, item):
        if isinstance(item, str):
            # testing by string name and not reference
            item_name = item
            find_me = self._parent.findChild(item_name)
            if find_me is not None:
                return True
            return False

        # testing by references
        for itm in self:
            if item is itm:
                return True

        return False

    def __eq__(self, other):
        equals = [
            len(self) == len(other),
        ]
        equals = equals + list(map(lambda x, y: x is y, iter(self), iter(other)))

        return all(equals)

    def __del__(self):
        self._parent.deleteLater()

    def push(self, command):
        if not isinstance(command, QObject):
            raise TypeError

        if command.parent() is not None:
            raise AttributeError('Command QObject already has a parent!')

        command.setParent(self._parent)
        command.setObjectName('Command_{}'.format(self._command_number))
        self._command_number += 1

    def pop(self):
        last_index = len(self) - 1
        last_guy = self._parent.children()[last_index]

        self._command_number -= 1
        last_guy.setParent(None)
        last_guy.setObjectName(None)
        return last_guy

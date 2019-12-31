# pylint: disable=no-name-in-module
from abc import abstractmethod
from PyQt5.QtCore import QObject

class CommandInterface:
    """ Interface for all commands that can be done, undone and redone.
    """
    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @data.setter
    @abstractmethod
    def data(self, value):
        pass

    @property
    @abstractmethod
    def old_data(self):
        pass

    @old_data.setter
    @abstractmethod
    def old_data(self, value):
        pass

    @property
    @abstractmethod
    def target(self):
        pass

    @target.setter
    @abstractmethod
    def target(self, value):
        pass

    @abstractmethod
    def operation(self):
        pass

    @abstractmethod
    def reverse_operation(self):
        pass

class Command(QObject, CommandInterface):
    """ Base class for all commands that can be done, undone, and redone.
    Implementation of the CommandInterface.
    """
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        target, data = kwargs.get('target', None), kwargs.get('data', None)
        old_data = kwargs.get('old_data', None)

        self._data = data
        self._old_data = old_data
        self._target = target

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def old_data(self):
        return self._old_data

    @old_data.setter
    def old_data(self, value):
        self._old_data = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    def operation(self):
        pass

    def reverse_operation(self):
        pass

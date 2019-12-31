# pylint: disable=no-name-in-module
# pylint: disable=len-as-condition
from PyQt5.QtCore import QObject, pyqtSignal
from .command import Command
from .stack import CommandStack

class AugerCommandManager(QObject):
    sig_undo_stack_changed = pyqtSignal(int)
    sig_redo_stack_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._undo_commands = CommandStack()
        self._redo_commands = CommandStack()

    def execute_new_command(self, command):
        if not isinstance(command, Command):
            raise TypeError('Commands must be auger.commands.Command!')

        command.operation()
        self._undo_commands.push(command)

        self.sig_undo_stack_changed.emit(len(self._undo_commands))

    def undo_last_command(self):
        if len(self._undo_commands) < 1:
            return

        command = self._undo_commands.pop()
        command.reverse_operation()
        self._redo_commands.push(command)

        self.sig_undo_stack_changed.emit(len(self._undo_commands))
        self.sig_redo_stack_changed.emit(len(self._redo_commands))

    def redo_last_command(self):
        if len(self._redo_commands) < 1:
            return

        command = self._redo_commands.pop()
        command.operation()
        self._undo_commands.push(command)

        self.sig_undo_stack_changed.emit(len(self._undo_commands))
        self.sig_redo_stack_changed.emit(len(self._redo_commands))

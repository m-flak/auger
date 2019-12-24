# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, QCoreApplication, QVariant, QEvent, pyqtSignal
from PyQt5.QtGui import QContextMenuEvent, QActionEvent
from PyQt5.QtWidgets import QPushButton, QAction
from ...app import get_app_instance

# Wow, so I pretty much reimplemented the QToolButton here.
# Amazing how there's so many ways to do things with QT.

class LanguageAction(QAction):
    sig_change_lang = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.triggered.connect(self.slot_trigger)
        self.sig_change_lang.connect(get_app_instance().ocr.slot_change_use_lang)

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_trigger(self):
        send_this = QActionEvent(
            QEvent.ActionChanged,
            self,
            None
        )
        QCoreApplication.sendEvent(self.parent(), send_this)

        # Show a bullet indicating selection
        if u'\u2022' not in self.text():
            self.setText(u'\u2022 {}'.format(self.text()))

        # Tell the OCR backend that 'Use' language has changed
        self.sig_change_lang.emit(self.data())

class AugerLanguageButton(QPushButton):
    def __init__(self, *args, **kwargs):
        def make_actions(languages):
            action = None
            for lang in languages.keys():
                action = LanguageAction(lang, self)
                action.setData(QVariant(lang))
                yield action
        # # # # #
        super().__init__(*args, **kwargs)

        self.addActions(list(make_actions(get_app_instance().ocr.languages)))

    def mark_active_language(self, language):
        """Mark the active language with a bullet point
        """
        our_actions = zip(
            self.actions(),
            [a.data() for a in self.actions()]
        )

        for action, data in our_actions:
            if language in data:
                if u'\u2022' not in action.text():
                    action.setText(u'\u2022 {}'.format(action.text()))
                break

    # Override method
    def mousePressEvent(self, mouse_event): # pylint: disable=invalid-name
        # Show the context menu with a left or right mouse click
        if mouse_event.buttons() & Qt.RightButton != Qt.RightButton:
            new_event = QContextMenuEvent(
                QContextMenuEvent.Mouse,
                mouse_event.pos(),
                mouse_event.globalPos(),
                mouse_event.modifiers()
            )
            QCoreApplication.sendEvent(self, new_event)

        return super().mousePressEvent(mouse_event)

    # Override method
    def actionEvent(self, action_event): # pylint: disable=invalid-name
        # Remove the bullets on prior selections
        if action_event.type() == QEvent.ActionChanged:
            if self.actions():
                for action in self.actions():
                    if action is action_event.action():
                        continue
                    action.setText(action.data())

        return super().actionEvent(action_event)

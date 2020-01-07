import pytest

from PyQt5.QtCore import Qt

from auger.document import TextDocument

@pytest.fixture
def original_text_contents(auger_window):
    original_text = auger_window.textSide_textEdit.toPlainText()
    original_html = auger_window.textSide_textEdit.toHtml()

    return original_text, original_html

class TestTabs:
    def test_tab_switch_no_changes(self, qtbot, auger_window,
                                   original_text_contents):
        orig_text = original_text_contents[0]
        orig_html = original_text_contents[1]

        tab_bar = auger_window.textSide_tabView
        txt_view = auger_window.textSide_textEdit
        htm_view = auger_window.textSide_htmlEdit

        with qtbot.waitSignal(tab_bar.tabBarClicked):
            tab_bar.tabBarClicked.emit(1) # Simulate a click
            assert txt_view.toPlainText() == orig_text
            assert htm_view.toPlainText() == txt_view.toHtml()
            assert htm_view.toPlainText() == orig_html

        with qtbot.waitSignal(tab_bar.tabBarClicked):
            tab_bar.tabBarClicked.emit(0) # Simulate a click
            assert htm_view.toPlainText() == orig_html
            assert htm_view.toPlainText() == txt_view.toHtml()

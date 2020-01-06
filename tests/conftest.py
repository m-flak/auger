import pytest
from auger.app import AugerApplication
from auger.forms.mainwindow import MainWindow

@pytest.fixture(scope='session')
def qapp(qapp):
    any_args = qapp.arguments()
    return AugerApplication(any_args)

@pytest.fixture
def auger_window(qtbot, qapp):
    window = MainWindow()
    if qapp.main_window is None:
        qapp.main_window = window
    if not hasattr(window, 'test_app_instance'):
        setattr(window, 'test_app_instance', qapp)
    window.show()
    qtbot.add_widget(window)
    return window

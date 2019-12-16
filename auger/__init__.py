from .app import AugerApplication
from .forms.mainwindow import MainWindow

__version__ = '0.0.1'

def create_auger():
    app = AugerApplication([])
    window = MainWindow()

    # Make the main window the same size as before
    win_w = app.settings.value('window_width', type=int)
    win_h = app.settings.value('window_height', type=int)
    if win_w > 0 and win_h > 0:
        window.resize(win_w, win_h)

    # Pick the ocr tool from settings (if possible)
    chosen_tool = app.settings.value('chosen_tool', type=str)
    if chosen_tool:
        app.ocr.tool = chosen_tool

    app.main_window = window

    return app, window

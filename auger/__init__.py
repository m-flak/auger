from .app import AugerApplication
from .forms.mainwindow import MainWindow
from .forms.resource import Resource, Resources

__version__ = '0.0.2'

def create_auger():
    app = AugerApplication([])
    window = MainWindow()

    # Set Application stylesheet
    sheet_file = Resources().resource(Resource.ResourceStyleSheet)
    with open(sheet_file, 'r') as f:
        app.setStyleSheet(f.read())

    # Make the main window the same size as before
    win_w = app.settings.value('window_width', type=int)
    win_h = app.settings.value('window_height', type=int)
    if win_w > 0 and win_h > 0:
        window.resize(win_w, win_h)

    # Maximize the window if it was before. >:(
    was_maximized = app.settings.value('was_maximized', type=bool)
    if was_maximized:
        window.setWindowState(
            window.windowState() | 0x00000002 # Qt::WindowMaximized
        )

    # Pick the ocr tool from settings (if possible)
    chosen_tool = app.settings.value('chosen_tool', type=str)
    if chosen_tool:
        app.ocr.tool = chosen_tool

    # Set current & fallback ocr languages (if possible)
    # Default / Fallback
    default_language = app.settings.value('default_language', type=str)
    if default_language:
        app.ocr.default_language = default_language

    # Current / Use
    use_language = app.settings.value('use_language', type=str)
    if use_language:
        app.ocr.use_language = use_language

    # Global reference to main window
    app.main_window = window

    return app, window

from .app import AugerApplication
from .forms.mainwindow import MainWindow

def create_auger():
    app = AugerApplication([])
    window = MainWindow()

    app.main_window = window

    return app, window

import sys
from auger import create_auger

if __name__ == '__main__':
    app, window = create_auger()
    window.show()
    sys.exit(app.exec_())

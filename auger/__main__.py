import sys
import auger

def main():
    app, window = auger.create_auger()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

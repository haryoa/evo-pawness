from PyQt5.QtWidgets import QApplication
from view.game_view_gui import ViewGUI
import sys

def main():
    app = QApplication(sys.argv)
    ex = ViewGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

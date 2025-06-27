import sys

from PySide6.QtWidgets import QApplication

from controller.temp_dir import TEMP_DIR_OBJ
from state import create_state, get_state
from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    create_state(app)
    get_state().new_project(name="New Project")
    window = MainWindow()
    window.show()
    exit_code = app.exec()
    TEMP_DIR_OBJ.cleanup()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

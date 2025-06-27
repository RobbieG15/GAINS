from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)

from controller.temp_dir import TEMP_DIR
from model.project.image import ImageObject
from state import get_state
from state.commands.image_commands import AddImageCommand
from state.progress_info import ProgressInfo
from view.ui.compiled.main_window import Ui_MainWindow
from view.widgets.image_item import ImageItem
from view.widgets.progress_item import ProgressItem
from view.widgets.viewer import MultiResolutionImageViewer


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.running_images: list[str] = []

        self.progress_widget = QDockWidget("Progress Tracker", self)
        self.progress_widget_body = QListWidget()
        self.progress_widget_body.setLayout(QVBoxLayout())
        self.progress_widget.setWidget(self.progress_widget_body)
        self.progress_widget.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.progress_widget)

        self.image_selector = QDockWidget("Image Selection", self)
        self.image_selector_body = QListWidget()
        self.image_selector.setWidget(self.image_selector_body)
        self.image_selector.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.addDockWidget(Qt.LeftDockWidgetArea, self.image_selector)

        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)

        self.action_import_image.triggered.connect(self.__on_import_image)
        self.action_new_project.triggered.connect(self.__on_new_project)
        self.action_open_project.triggered.connect(lambda _: self.__on_open_project())
        self.action_save_as.triggered.connect(self.__on_save_as)
        self.action_save_project.triggered.connect(self.__on_save)
        self.action_exit.triggered.connect(self.__on_exit)
        self.actions_annotations.triggered.connect(self.__on_toggle_annotations)

        get_state().project_changed.connect(self.__on_project_changed)

    def __on_import_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Whole-Slide Image (.svs)",
            "",
            "SVS images (*.svs)",
            options=QFileDialog.Option.ReadOnly,
        )
        if file_path is None or file_path == "":
            return
        command = AddImageCommand(file_path)
        get_state().execute_command(command)

    def __on_exit(self):
        state = get_state()
        if not state.unsaved_changes() or self.__handle_unsaved_changes():
            app = QApplication.instance()
            if app is not None:
                app.quit()
            else:
                self.close()

    def __on_new_project(self):
        state = get_state()
        if not state.unsaved_changes() or self.__handle_unsaved_changes():
            state.new_project()

    def __on_open_project(self, filepath: str | None = None):
        state = get_state()
        if not state.unsaved_changes() or self.__handle_unsaved_changes():
            if filepath is None:
                path, _ = QFileDialog.getOpenFileName(
                    self,
                    caption="Select a project file",
                    dir="",
                    filter="Project File (*.proj)",
                    options=QFileDialog.Option.ReadOnly,
                )
                if path is None or path == "":
                    return
                filepath = path

            state.load(filepath)

    def __on_save_as(self):
        state = get_state()
        path, _ = QFileDialog.getSaveFileName(
            self,
            caption="Select a project file",
            dir="",
            filter="Project File (*.proj)",
            options=QFileDialog.Option.ReadOnly,
        )
        if path is None or path == "":
            return

        state.save(path)
        self.__on_open_project(filepath=path)
        state.project.save_path = path

    def __on_save(self):
        state = get_state()
        if state.project.save_path == "":
            self.__on_save_as()
        if state.project.save_path != "":
            state.save(state.project.save_path)

    def __on_toggle_annotations(self) -> None:
        central_widget = self.centralWidget()
        if central_widget is not None and isinstance(
            central_widget, MultiResolutionImageViewer
        ):
            central_widget.toggle_annotations()

    def __handle_unsaved_changes(self) -> bool:
        choice = QMessageBox.warning(
            self,
            "Unsaved Changes",
            "Your project has unsaved changes.\nDo you want to save them before continuing?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )
        if choice == QMessageBox.StandardButton.Save:
            self.__on_save()
        elif choice == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def __on_process_done(self, id: str) -> None:
        self.running_images.remove(id)
        images = get_state().project.images
        for image in images:
            if image.id == id:
                item = QListWidgetItem(self.image_selector_body)
                item_widget = ImageItem(image, self.image_selector_body)
                item.setSizeHint(item_widget.sizeHint())
                self.image_selector_body.setMinimumWidth(item_widget.minimumWidth())
                item_widget.view_image_btn.clicked.connect(
                    lambda: self.__view_image(image)
                )
                self.image_selector_body.setItemWidget(item, item_widget)
                break

    def __view_image(self, image: ImageObject) -> None:
        old = self.takeCentralWidget()
        if old is not None:
            old.deleteLater()
        viewer = MultiResolutionImageViewer(TEMP_DIR.joinpath(image.name), parent=self)
        self.setCentralWidget(viewer)

    def __remove_progress_item(self, item: QListWidgetItem) -> None:
        row = self.progress_widget_body.row(item)
        if row == -1:
            return

        widget = self.progress_widget_body.itemWidget(item)
        if widget is not None:
            self.progress_widget_body.removeItemWidget(item)
            widget.deleteLater()
        self.progress_widget_body.takeItem(row)

    def __on_project_changed(self) -> None:
        images = get_state().project.images
        for image in images:
            if not image.loaded and image.id not in self.running_images:
                info = ProgressInfo(image.name, image)
                item = QListWidgetItem(self.progress_widget_body)
                item_widget = ProgressItem(info, self.progress_widget_body)
                self.progress_widget_body.setMinimumWidth(item_widget.minimumWidth())
                item.setSizeHint(item_widget.sizeHint())
                self.progress_widget_body.setItemWidget(item, item_widget)
                item_widget.item_finished.connect(self.__on_process_done)
                item_widget.item_finished.connect(
                    lambda _: self.__remove_progress_item(item)
                )
                self.progress_widget_body.layout().addWidget(item_widget)
                self.running_images.append(image.id)

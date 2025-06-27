from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMessageBox, QWidget

from controller.temp_dir import TEMP_DIR
from controller.workflow import start_image_processing
from state.progress_info import ProgressInfo
from view.ui.compiled.widgets.progress_item import Ui_Form
from view.utils.worker import WorkerThread


class ProgressItem(QWidget, Ui_Form):
    item_finished: Signal = Signal(str)

    def __init__(self, progress_info: ProgressInfo, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.progress_info: ProgressInfo = progress_info

        self.progress_info.progress_changed.connect(self.__on_progress_changed)
        self.__on_progress_changed()

        self.__start_worker_thread(
            start_image_processing,
            progress_info.image.save_path,
            TEMP_DIR.joinpath(Path(progress_info.image.save_path).stem).as_posix(),
            TEMP_DIR.joinpath(f"{progress_info.image.name}_inference").as_posix(),
            self.progress_info,
        )

    def __on_progress_changed(self) -> None:
        self.status_box.setTitle(f"Image {self.progress_info.name}")
        self.status_label.setText(self.progress_info.status)
        self.progress_bar.setValue(self.progress_info.percent_complete)

    def __start_worker_thread(self, fn, *args, **kwargs):
        self._worker_thread = WorkerThread(fn, *args, **kwargs)
        self._worker_thread.error_occurred.connect(self.__show_error)
        self._worker_thread.finished_signal.connect(self.__on_job_done)
        self._worker_thread.start()

    def __show_error(self, msg: str):
        QMessageBox.critical(self, f"Error processing {self.progress_info.name}", msg)

    def __on_job_done(self) -> None:
        self.progress_info.image.loaded = True
        self.item_finished.emit(self.progress_info.image.id)

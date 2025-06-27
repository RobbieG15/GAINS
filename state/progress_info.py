from PySide6.QtCore import QObject, Signal

from model.project.image import ImageObject


class ProgressInfo(QObject):
    progress_changed: Signal = Signal()

    def __init__(self, name: str, image: ImageObject, parent: QObject = None):
        super().__init__(parent)
        self.name: str = name
        self.image: ImageObject = image
        self.status: str = "Queued"
        self.percent_complete: int = 0

from PySide6.QtWidgets import QHBoxLayout, QWidget

from model.project.image import ImageObject
from view.ui.compiled.widgets.image_item import Ui_Form


class ImageItem(QWidget, Ui_Form):
    def __init__(self, image: ImageObject, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.image_box.setTitle(image.name)
        self.path_label.setText(image.save_path)
        self.preview_widget.setLayout(QHBoxLayout())

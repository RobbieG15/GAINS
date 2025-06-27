from model.project import ProjectObject
from model.project.image import ImageObject


class ProjectFile(ProjectObject):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.save_path: str = ""
        self.images: list[ImageObject] = []

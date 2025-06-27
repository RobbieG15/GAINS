from model.project import ProjectObject
from model.project.tile import TileObject


class ImageObject(ProjectObject):
    def __init__(self, name: str, save_path: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.save_path: str = save_path
        self.loaded: bool = False
        self.tiles: dict[int, list[TileObject]] = {}

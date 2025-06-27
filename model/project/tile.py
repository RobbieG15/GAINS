from model.project import ProjectObject


class TileObject(ProjectObject):
    def __init__(self, name: str, rel_path: str, x: int, y: int, **kwargs):
        super().__init__(name=name, **kwargs)
        self.save_path: str = rel_path
        self.x: int = x
        self.y: int = y

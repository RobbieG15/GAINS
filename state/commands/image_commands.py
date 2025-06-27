from pathlib import Path

from model.project.image import ImageObject
from state.commands import Command


class AddImageCommand(Command):
    def __init__(self, save_path: str):
        self.image = ImageObject(Path(save_path).stem, save_path)

    def execute(self, state_manager):
        state_manager.project.images.append(self.image)

    def undo(self, state_manager):
        state_manager.project.images.remove(self.image)

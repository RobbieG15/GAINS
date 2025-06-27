import json
from copy import deepcopy

from PySide6.QtCore import QObject, Signal

from model.project.project_file import ProjectFile
from state.commands import Command


class StateManager(QObject):
    project_changed = Signal()
    undo_redo_changed = Signal()
    project_saved = Signal()
    project_loaded = Signal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.project: ProjectFile | None = None
        self.save_project: ProjectFile | None = None
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

    def unsaved_changes(self):
        return self.project.to_json() != self.save_project.to_json()

    def new_project(self, name: str = "New Project"):
        self.project = ProjectFile(name=name)
        self.save_project = deepcopy(self.project)
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.project_changed.emit()
        self.undo_redo_changed.emit()

    def execute_command(self, cmd: Command):
        cmd.execute(self)
        self.undo_stack.append(cmd)
        self.redo_stack.clear()
        self.undo_redo_changed.emit()
        self.project_changed.emit()

    def undo(self):
        if self.undo_stack:
            cmd = self.undo_stack.pop()
            cmd.undo(self)
            self.redo_stack.append(cmd)
            self.undo_redo_changed.emit()
            self.project_changed.emit()

    def redo(self):
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.redo(self)
            self.undo_stack.append(cmd)
            self.undo_redo_changed.emit()
            self.project_changed.emit()

    def save(self, filepath: str):
        if not self.project:
            raise RuntimeError("No project to save.")
        with open(filepath, "w") as f:
            f.write(self.project.to_json())
        self.save_project = deepcopy(self.project)
        self.project_saved.emit()

    def load(self, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)
        self.project = ProjectFile.from_dict(data)
        self.save_project = deepcopy(self.project)
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.project_loaded.emit(filepath)
        self.project_changed.emit()
        self.undo_redo_changed.emit()


_state: StateManager | None = None


def create_state(parent: QObject | None = None) -> StateManager:
    global _state
    if _state is not None:
        raise RuntimeError("StateManager already created; use get_state().")
    _state = StateManager(parent)
    return _state


def get_state() -> StateManager:
    if _state is None:
        raise RuntimeError("StateManager not yet created; call create_state() first.")
    return _state

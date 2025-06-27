from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, state_manager):
        pass

    @abstractmethod
    def undo(self, state_manager):
        pass

    def redo(self, state_manager):
        self.execute(state_manager)

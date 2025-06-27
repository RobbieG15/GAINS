import traceback

from PySide6.QtCore import QThread, Signal


class WorkerThread(QThread):
    """
    Generic QThread that runs a callable with args and kwargs.

    Emits:
        - finished_signal(): when callable completes (success or error)
        - result_ready(object): with the return value if any
        - error_occurred(str): with exception message if an error happens
    """

    finished_signal = Signal()
    result_ready = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self._result = None

    def run(self):
        try:
            self._result = self.fn(*self.args, **self.kwargs)
            self.result_ready.emit(self._result)
        except Exception as e:
            traceback.print_exc()
            self.error_occurred.emit(str(e))
        finally:
            self.finished_signal.emit()

    def result(self):
        return self._result

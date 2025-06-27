import tempfile
from pathlib import Path

TEMP_DIR_OBJ = tempfile.TemporaryDirectory()
TEMP_DIR = Path(TEMP_DIR_OBJ.name)

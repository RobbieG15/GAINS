import threading
from pathlib import Path

from controller.infer_controller import infer
from controller.wsi_controller import generate_tiles
from state.progress_info import ProgressInfo

MAX_RUNNING = 1
SEMAPHORE = threading.BoundedSemaphore(MAX_RUNNING)


def start_image_processing(
    svs_path: str,
    base_tile_out_dir: str,
    infer_tile_out_dir: str,
    progress_info: ProgressInfo,
    *,
    tile_size: int = 512,
    model_path: str = Path("assets")
    .joinpath("ai_models", "old_best_checkpoint.ckpt")
    .as_posix(),
) -> None:
    with SEMAPHORE:
        generate_tiles(svs_path, base_tile_out_dir, tile_size, progress_info)
        infer(
            Path(base_tile_out_dir).joinpath("level0").as_posix(),
            infer_tile_out_dir,
            model_path,
            progress_info,
        )
        progress_info.status = "Processing complete"
        progress_info.percent_complete = 100
        progress_info.progress_changed.emit()

import math
import os
from pathlib import Path
from typing import Tuple

import numpy as np
import openslide
from PIL import Image

from controller.image_controller import __mostly_white
from state.progress_info import ProgressInfo


def generate_tiles(
    svs_path: str | os.PathLike,
    out_dir: str | os.PathLike,
    tile_size: int,
    progress_info: ProgressInfo,
) -> None:
    svs_path = Path(svs_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slide = openslide.OpenSlide(svs_path)

    for level_idx in range(slide.level_count):
        progress_info.status = f"Tiling level {level_idx}"
        progress_info.percent_complete = 0
        progress_info.progress_changed.emit()

        level_out = out_dir / f"level{level_idx}"
        level_out.mkdir(parents=True, exist_ok=True)

        # ── determine stride & request size for this level ──────────────
        if level_idx == 0:
            stride = tile_size * 2  # move 1024 px per tile in source
            request_wh: Tuple[int, int] = (stride, stride)
        else:
            stride = tile_size  # native stride
            request_wh = (tile_size, tile_size)

        level_w, level_h = slide.level_dimensions[level_idx]
        cols = math.ceil(level_w / stride)
        rows = math.ceil(level_h / stride)
        total_iterations = cols * rows
        current_iteration = 0

        downsample = slide.level_downsamples[level_idx]  # 1.0 at level-0

        for row in range(rows):
            for col in range(cols):
                # top-left of the region in THIS level’s coords
                x_lv = col * stride
                y_lv = row * stride

                # convert to level-0 coords for read_region()
                x0 = int(x_lv * downsample)
                y0 = int(y_lv * downsample)

                # ── read & save ─────────────────────────────────────────
                img = slide.read_region((x0, y0), level_idx, request_wh)
                if __mostly_white(
                    np.array(img), white_cutoff=235, max_white_ratio=0.97
                ):
                    current_iteration += 1
                    progress_info.percent_complete = int(
                        current_iteration / total_iterations * 100
                    )
                    progress_info.status = str(
                        f"Tiling level {level_idx} ({current_iteration}/{total_iterations})"
                    )
                    progress_info.progress_changed.emit()
                    continue
                # Replace black transparent padding with white
                bg = Image.new("RGB", img.size, (255, 255, 255))
                img = Image.alpha_composite(bg.convert("RGBA"), img).convert("RGB")

                if level_idx == 0:
                    img = img.resize((tile_size, tile_size), Image.Resampling.LANCZOS)

                img.save(level_out / f"tile_{row}_{col}.png", format="PNG")

                current_iteration += 1
                progress_info.percent_complete = int(
                    current_iteration / total_iterations * 100
                )
                progress_info.status = str(
                    f"Tiling level {level_idx} ({current_iteration}/{total_iterations})"
                )
                progress_info.progress_changed.emit()

    slide.close()

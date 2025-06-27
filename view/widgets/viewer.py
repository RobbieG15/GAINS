import math
from pathlib import Path

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QImage, QPainter, QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView


class MultiResolutionImageViewer(QGraphicsView):
    """
    Tile viewer for folders laid out as:
        tiles_root/
            level0/         <- highest-res
            level1/
            ...
            levelN/         <- lowest-res (fewest tiles)

    Each level folder contains 512×512 PNGs named  tile_<row>_<col>.png
    """

    TILE_SIZE = 512  # physical tile edge length in *level-pixel* units
    MIN_TILE_SCREEN = 128  # px – if smaller, switch to lower-res level
    MAX_TILE_SCREEN = 512  # px – if bigger, switch to higher-res level
    ZOOM_BASE = 1.0015  # < 1.0 slower, >1.0 faster
    MIN_SCALE = 0.03  # keep user from zooming out forever
    MAX_SCALE = 64.0  # and from zooming into oblivion
    WHITE_CUTOFF = 245  # ≥ this on every channel counts as white
    OVERLAY_OPACITY = 0.40  # Overlay opacity (40%)

    # ────────────────────────────────────────────────────────────────
    # ctor
    # ────────────────────────────────────────────────────────────────
    def __init__(self, tiles_root: Path, parent=None):
        super().__init__(parent)

        self.tiles_root = tiles_root
        self.inference_root = tiles_root.parent.joinpath(tiles_root.stem + "_inference")
        self.annotations = True

        self._discover_levels()  # populates self.level_paths, self.level_sizes

        self.setRenderHints(self.renderHints() | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # tile cache {(level,row,col): QGraphicsPixmapItem}
        self._tiles = {}

        # start at lowest-resolution overview (largest level index)
        self._current_level = len(self.level_paths) - 1
        self._set_scene_rect_for_level(self._current_level)
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        # ensure visible tiles show up
        self._update_visible_tiles()

    # ────────────────────────────────────────────────────────────────
    # level discovery helpers
    # ────────────────────────────────────────────────────────────────
    def _discover_levels(self):
        """Find level folders and their pixel sizes."""
        paths = sorted(
            [
                p
                for p in self.tiles_root.iterdir()
                if p.is_dir() and p.name.startswith("level")
            ],
            key=lambda p: int(p.name[5:]),
        )
        if not paths:
            raise RuntimeError(f"No level* folders in {self.tiles_root}")

        self.level_paths = paths
        self.level_sizes = []
        for lp in self.level_paths:
            # find width/height by scanning filenames
            w = h = -1
            for tile in lp.glob("tile_*.png"):
                _, r, c = tile.stem.split("_")
                w = max(w, int(c))
                h = max(h, int(r))
            self.level_sizes.append(
                ((w + 1) * self.TILE_SIZE, (h + 1) * self.TILE_SIZE)
            )

    # ────────────────────────────────────────────────────────────────
    # event overrides
    # ────────────────────────────────────────────────────────────────
    def wheelEvent(self, ev):
        """Smooth, accelerator-like zoom centred on the cursor."""
        # 1. angleDelta is in eighths of a degree → ±120 per notch on most mice
        delta = ev.angleDelta().y()
        if delta == 0:
            return

        # 2. Continuous factor:   factor = base ** delta
        #    • +120 → ×1.197  (≈+20 %)
        #    • -120 → ×0.835  (≈-17 %)
        factor = math.pow(self.ZOOM_BASE, delta)

        # 3. Clamp overall scale so we don’t go infinite in/out
        current_scale = self.transform().m11()  # m11 == m22; isotropic
        new_scale = current_scale * factor
        if new_scale < self.MIN_SCALE:
            factor = self.MIN_SCALE / current_scale
        elif new_scale > self.MAX_SCALE:
            factor = self.MAX_SCALE / current_scale

        # 4. Zoom under mouse
        self.scale(factor, factor)

        # 5. Update tiles / level
        self._maybe_change_level()
        self._update_visible_tiles()

        ev.accept()

    def toggle_annotations(self) -> None:
        self.annotations = not self.annotations
        self._update_visible_tiles(reset=True)

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self._update_visible_tiles()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self._maybe_change_level()
        self._update_visible_tiles()

    # ────────────────────────────────────────────────────────────────
    # level management
    # ────────────────────────────────────────────────────────────────
    def _maybe_change_level(self):
        """Pick appropriate level based on how big a tile currently appears."""
        # size of one tile in *viewport* pixels
        one_tile_scene = self.mapFromScene(
            QRectF(0, 0, self.TILE_SIZE, self.TILE_SIZE)
        ).boundingRect()
        tile_px = one_tile_scene.width()

        level = self._current_level
        if tile_px < self.MIN_TILE_SCREEN and level < len(self.level_paths) - 1:
            level += 1  # go to lower-res level
        elif tile_px > self.MAX_TILE_SCREEN and level > 0:
            level -= 1  # go to higher-res level

        if level != self._current_level:
            self._swap_level(level)

    def _swap_level(self, new_level: int):
        """Switch level, keeping the *relative* viewport centre."""
        old_rect = self.scene.sceneRect()
        if old_rect.width() <= 0 or old_rect.height() <= 0:
            return

        # 1. where is the view centre in scene coords?
        centre_scene = self.mapToScene(self.viewport().rect().center())

        # 2. express it as fractions of the old scene
        fx = (centre_scene.x() - old_rect.left()) / old_rect.width()
        fy = (centre_scene.y() - old_rect.top()) / old_rect.height()

        # 3. update level & scene rect
        self._current_level = new_level
        self._set_scene_rect_for_level(new_level)
        new_rect = self.scene.sceneRect()

        # 4. convert fractions back to absolute coords in new scene
        new_centre = QPointF(
            new_rect.left() + fx * new_rect.width(),
            new_rect.top() + fy * new_rect.height(),
        )

        # 5. clear old tiles, keep viewport anchored
        for item in self._tiles.values():
            self.scene.removeItem(item)
        self._tiles.clear()

        self.centerOn(new_centre)

    def _set_scene_rect_for_level(self, lvl: int):
        w, h = self.level_sizes[lvl]
        self.scene.setSceneRect(0, 0, w, h)
        print(f"Setting scene to {lvl}")

    # ────────────────────────────────────────────────────────────────
    # tile loading / purging
    # ────────────────────────────────────────────────────────────────
    def _update_visible_tiles(self, reset: bool = False):
        """Ensure tiles intersecting viewport are loaded; others dropped."""
        if reset:
            self._tiles = {}
        lvl = self._current_level
        lvl_path = self.level_paths[lvl]

        # visible rectangle in *scene* coords
        vis_rect = self.mapToScene(self.viewport().rect()).boundingRect()

        r0 = int(vis_rect.top() // self.TILE_SIZE)
        r1 = int(math.ceil(vis_rect.bottom() / self.TILE_SIZE))
        c0 = int(vis_rect.left() // self.TILE_SIZE)
        c1 = int(math.ceil(vis_rect.right() / self.TILE_SIZE))

        # drop caches outside view
        to_remove = [
            key
            for key in self._tiles
            if key[0] != lvl
            or key[1] < r0
            or key[1] >= r1
            or key[2] < c0
            or key[2] >= c1
        ]
        for key in to_remove:
            self.scene.removeItem(self._tiles[key])
            del self._tiles[key]

        # add missing visible tiles
        for r in range(r0, r1):
            for c in range(c0, c1):
                key = (lvl, r, c)
                if key in self._tiles:
                    continue
                tile_file = lvl_path / f"tile_{r}_{c}.png"
                if not tile_file.exists():
                    continue
                pix = self._composited_pixmap(self._current_level, r, c)
                item = QGraphicsPixmapItem(pix)
                item.setPos(c * self.TILE_SIZE, r * self.TILE_SIZE)
                self.scene.addItem(item)
                self._tiles[key] = item

    def _composited_pixmap(self, level: int, row: int, col: int) -> QPixmap:
        """
        Return the base tile with inference overlay (level 0 only).
        White pixels in the inference tile become fully transparent.
        Non-transparent pixels are recolored red before compositing.
        """
        base_path = self.level_paths[level] / f"tile_{row}_{col}.png"
        if base_path.exists():
            base_pix = QPixmap(base_path.as_posix())
        else:
            base_pix = QPixmap(512, 512)
            base_pix.fill(Qt.GlobalColor.white)

        # Only apply overlay for level 0 and if inference_root is set
        if level != 0 or not self.annotations or not self.inference_root:
            return base_pix

        inf_path = self.inference_root / base_path.name
        if not inf_path.exists():
            return base_pix

        # Load inference image and convert to ARGB32 format
        inf_img = (
            QImage(inf_path.as_posix())
            .convertToFormat(QImage.Format.Format_ARGB32)
            .scaled(
                base_pix.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        if inf_img.isNull():
            return base_pix

        # Access pixel data as numpy array
        ptr = inf_img.bits()
        arr = np.array(ptr, copy=False).reshape((inf_img.height(), inf_img.width(), 4))

        # Make white pixels fully transparent
        rgb = arr[..., :3]
        white_mask = (rgb >= self.WHITE_CUTOFF).all(axis=-1)
        arr[..., 3][white_mask] = 0  # Set alpha channel to 0 where white

        # Recolor all non-transparent pixels to red (R=255, G=0, B=0)
        non_transparent_mask = arr[..., 3] > 0
        arr[..., 0][non_transparent_mask] = 255  # Red channel
        arr[..., 1][non_transparent_mask] = 0  # Green channel
        arr[..., 2][non_transparent_mask] = 0  # Blue channel

        inf_pix = QPixmap.fromImage(inf_img)

        # Composite overlay with base tile at specified opacity
        composite = QPixmap(base_pix.size())
        composite.fill(Qt.transparent)

        painter = QPainter(composite)
        painter.drawPixmap(0, 0, base_pix)
        painter.setOpacity(self.OVERLAY_OPACITY)
        painter.drawPixmap(0, 0, inf_pix)
        painter.end()

        return composite

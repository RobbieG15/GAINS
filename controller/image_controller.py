import numpy as np


def __mostly_white(
    img: np.ndarray, white_cutoff: int = 245, max_white_ratio: float = 0.98
) -> bool:
    if img.ndim == 3 and img.shape[-1] in (4, 3):  # RGB(A)
        channels = img[..., :3]  # ignore alpha if present
    else:  # grayscale
        channels = img

    # Normalise cutoff for float images
    if np.issubdtype(img.dtype, np.floating):
        cutoff = white_cutoff / 255.0
    else:
        cutoff = white_cutoff

    # Pixel is white only if ALL channels exceed cutoff
    white_mask = (
        np.all(channels > cutoff, axis=-1) if channels.ndim == 3 else channels > cutoff
    )

    white_ratio = white_mask.mean()
    return white_ratio >= max_white_ratio

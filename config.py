import torch

# determine the device to be used for training and evaluation
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# determine if we will be pinning memory during data loading
PIN_MEMORY: bool = True if DEVICE == "cuda" else False

# define the input image dimensions
INPUT_IMAGE_WIDTH: int = 512
INPUT_IMAGE_HEIGHT: int = 512

# Post Processing
CUTOFF = 0.5

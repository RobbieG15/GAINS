from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

import config
from controller.image_controller import __mostly_white
from model.ai_models.nested_unet import NestedUNet as UNet
from state.progress_info import ProgressInfo


def __load_model(model_path: Path, device: torch.device, out_size: tuple[int, int]):
    if model_path.suffix == ".pth":
        # Full model file
        model = torch.load(model_path, map_location=device, weights_only=False)
    else:
        # Checkpoint with state_dict
        model = UNet(outSize=out_size).to(device)
        checkpoint = torch.load(model_path, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model


def __get_image_paths(input_path: Path):
    if input_path.is_dir():
        return sorted([p for p in input_path.glob("*.png") if "_mask" not in p.stem])
    elif input_path.is_file():
        return [input_path]
    else:
        raise ValueError(f"Invalid input path: {input_path}")


def __preprocess_image(image_path: Path, transform):
    img = Image.open(image_path).convert("RGB")
    return transform(img)


def run_inference(
    model,
    image_paths,
    transform,
    output_dir: str,
    progress_info: ProgressInfo,
):
    output_dir = Path(output_dir)
    device = config.DEVICE
    output_dir.mkdir(parents=True, exist_ok=True)

    progress_info.status = "Running inference"
    progress_info.progress_changed.emit()
    for i, img_path in enumerate(image_paths):
        img_tensor = __preprocess_image(img_path, transform).to(device)
        if __mostly_white(
            img_tensor.detach().cpu().numpy(), white_cutoff=235, max_white_ratio=0.97
        ):
            progress_info.percent_complete = int(i / len(image_paths) * 100)
            progress_info.status = str(f"Running inference ({i}/{len(image_paths)})")
            progress_info.progress_changed.emit()
            continue
        img_tensor_batch = img_tensor.unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            logits = model(img_tensor_batch)
            pred = (torch.sigmoid(logits) > config.CUTOFF).squeeze().cpu().numpy()

        # mask_np = __postprocess_mask(pred)
        mask_np = pred * 255
        if __mostly_white(mask_np):
            progress_info.percent_complete = int(i / len(image_paths) * 100)
            progress_info.status = str(f"Running inference ({i}/{len(image_paths)})")
            progress_info.progress_changed.emit()
            continue

        # Save predicted mask
        output_path = output_dir.joinpath(f"{img_path.stem}.png").as_posix()
        mask_img = Image.fromarray((mask_np).astype(np.uint8))
        mask_img.save(output_path)
        progress_info.percent_complete = int(i / len(image_paths) * 100)
        progress_info.status = str(f"Running inference ({i}/{len(image_paths)})")
        progress_info.progress_changed.emit()


def infer(
    input_path: str,
    output_dir: str,
    model_path: str,
    progress_info: ProgressInfo,
):
    input_image_height = config.INPUT_IMAGE_HEIGHT
    input_image_width = config.INPUT_IMAGE_WIDTH

    progress_info.status = "Starting inference"
    progress_info.percent_complete = 0
    progress_info.progress_changed.emit()

    # Define the same preprocessing used in training
    transform = transforms.Compose(
        [
            transforms.Resize((input_image_height, input_image_width)),
            transforms.ToTensor(),
        ]
    )

    device = config.DEVICE
    model = __load_model(
        Path(model_path), device, (input_image_height, input_image_width)
    )
    image_paths = __get_image_paths(Path(input_path))
    run_inference(model, image_paths, transform, output_dir, progress_info)

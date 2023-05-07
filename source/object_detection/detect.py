from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw

from utils.augmentations import letterbox
from .yolov5.models.common import DetectMultiBackend
from .yolov5.utils.general import (
    non_max_suppression,
    scale_boxes,
)
from .yolov5.utils.torch_utils import select_device


def detect(
    img,  # np.ndarray
    img_name,
    model_file,  # path to .pt or .pth file
    device=None,
    img_size=(640, 640),
    # NMS configs
    confidence_threshold=0.25,
    iou_threshold=0.45,
    classes=None,  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False,
    max_det=1000,

):
    if device is None:
        device = select_device(device)

    model = DetectMultiBackend(
        model_file,
        device=device
    )
    stride, names, pt = model.stride, model.names, model.pt
    batch_size = 1

    # Warm up the model by running it on an empty array
    model.warmup(
        imgsz=(1 if pt or model.triton else batch_size, 3, *img_size)
    )

    # Pre-process an image: resize, padding, ...etc
    preprocessed_img = letterbox(
        img,
        new_shape=img_size,
        stride=stride,
        auto=False,  # False doesn't preserve the image ratio, sets the resolution we intended
    )[0]

    preprocessed_img = preprocessed_img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    preprocessed_img = np.ascontiguousarray(preprocessed_img)

    preprocessed_img = torch.from_numpy(preprocessed_img).to(model.device)
    preprocessed_img = preprocessed_img.half() if model.fp16 else preprocessed_img.float()

    preprocessed_img /= 255  # 0-255 to 0.0-1.0 image normalization
    preprocessed_img = preprocessed_img[None]  # expand to batch dim

    # Inference
    predictions = model(preprocessed_img)
    predictions = non_max_suppression(
        predictions,
        confidence_threshold,
        iou_threshold,
        classes,
        agnostic_nms,
        max_det=max_det
    )

    result = []
    detected_objects = predictions[0]
    static_output_path = None

    if len(detected_objects):
        detected_objects[:, :4] = scale_boxes(preprocessed_img.shape[2:], detected_objects[:, :4], img.shape).round()

        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        for detected_object in detected_objects:
            bounding_box = detected_object[:4].numpy().astype(int).tolist()
            bounding_box = [bounding_box[:2], bounding_box[2:4]]
            confidence_score = float(detected_object[4])
            cls = int(detected_object[5])

            detected_object_dict = {
                'bounding_box': bounding_box,
                'confidence_score': confidence_score,
                'class_id': cls,
                'class_label': None,
            }

            result.append(detected_object_dict)
        # Draw bounding boxes and class labels on the input image
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        for detected_object in result:
            bounding_box = detected_object['bounding_box']
            class_label = detected_object['class_label']
            class_id = detected_object['class_id']
            x1, y1 = bounding_box[0]
            x2, y2 = bounding_box[1]

            # Draw rectangle around the object
            draw.rectangle([tuple(bounding_box[0]), tuple(bounding_box[1])], outline=(0, 255, 0), width=8)

            # Draw class label and confidence score
            label_text = f"{names[class_id]} {detected_object['confidence_score']:.2f}"
            draw.text((x1, y1 - 20), label_text, fill=(0, 255, 0), font=None)

        # Save the output image to a desired location using PIL
        output_path = Path('results') / f"{img_name.replace('.jpg', '')}_result.jpg"
        static_output_path = Path('uploads') / output_path
        img_pil.save(str(static_output_path))

    return result, static_output_path

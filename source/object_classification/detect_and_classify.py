from pathlib import Path

from PIL import Image as PIL_Image
import numpy as np

from .classify import classify_images
from object_detection.detect import detect


def crop_plates(
    img,
    plates
):
    cropped_plate_images = []

    for plate in plates:
        box = plate['bounding_box']
        cropped_plate_img = img[box[0][1]:box[1][1], box[0][0]:box[1][0]]
        cropped_plate_images.append(cropped_plate_img)

    return cropped_plate_images


def detect_and_classify(
    image,  # path to image
    image_name,
    yolov5_model_file,  # path to .pt or .pth file
    classifier_model_file,  # path to .pt or .pth file
    classes,  # list of classifier's classes
):
    img = np.array(PIL_Image.open(image))

    plates, result_img = detect(
        img,
        img_name=image_name,
        model_file=yolov5_model_file
    )

    cropped_plate_images = crop_plates(
        img,
        plates
    )

    predicted_classes = classify_images(
        cropped_plate_images,
        model_file=classifier_model_file
    )

    for plate, predicted_class in zip(plates, predicted_classes):
        plate['class_id'] = predicted_class
        plate['class_label'] = classes[predicted_class]

    return plates, result_img


if __name__ == '__main__':
    YOLOV5_MODEL_FILE = Path('food_detection/yolov5s_food_epochs100_freeze8/weights/best.pt')
    CLASSIFIER_MODEL_FILE = Path('food_classification/resnet50_food.pt')
    CLASSES_FILE = Path('food_classification/classes.txt')
    IMG = Path('food_detection/test_japanese_food.jpeg')

    with open(CLASSES_FILE, 'r') as f:
        classes = f.read().split()

    output = detect_and_classify(
        IMG,
        yolov5_model_file=YOLOV5_MODEL_FILE,
        classifier_model_file=CLASSIFIER_MODEL_FILE,
        classes=classes
    )
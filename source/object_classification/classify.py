from pathlib import Path

from PIL import Image as PIL_Image
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import transforms


# ImageNet transform
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# Define a custom dataset class to load the images
class ImageDataset(Dataset):
    def __init__(self, images, transform=None):
        self.images = images
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        if self.transform:
            image = self.transform(image)
        return image


def classify_image(
    img,  # np.ndarray
    model_file,  # path to .pt or .pth file
):
    transformed_img = transform(img)
    transformed_img = transformed_img.unsqueeze(0)  # add dimension

    model = torch.load(model_file)
    model.eval()

    with torch.no_grad():
        output = model(transformed_img)

    _, predicted = torch.max(output, 1)

    return predicted.item()


def classify_images(
    images,  # list[np.ndarray]
    model_file,  # path to .pt or .pth file
):
    dataset = ImageDataset(images, transform)

    # Define the dataloader
    max_batch_size = 16
    batch_size = max(len(dataset), max_batch_size)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    model = torch.load(model_file)
    model.eval()

    result = []

    with torch.no_grad():
        for images_batch in dataloader:
            outputs = model(images_batch)

            # Convert the outputs to probabilities using softmax
            probs = torch.nn.functional.softmax(outputs, dim=1)

            # Get the indices of max values
            predicted_classes = probs.argmax(dim=1).tolist()

            result.extend(predicted_classes)

    return result


if __name__ == '__main__':
    ROOT_DIR = Path('food_classification')

    SOURCE_IMG = ROOT_DIR / 'test_steak.jpeg'
    MODEL_FILE = ROOT_DIR / 'resnet50_food.pt'

    img = np.array(PIL_Image.open(SOURCE_IMG))

    output = classify_image(
        img,
        MODEL_FILE
    )

    img2 = np.array(PIL_Image.open(ROOT_DIR / 'test_spaghetti.jpeg'))
    images = [img, img2]

    output = classify_images(
        images,
        MODEL_FILE
    )

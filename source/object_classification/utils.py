from PIL import Image


def crop_image(image_path, output_path, txt_file_path, file_name):
    # Open the image using PIL
    img = Image.open(image_path)

    # Read the YOLO coordinates from the text file
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through the lines and parse the coordinates
    for i, line in enumerate(lines):
        values = line.strip().split()
        class_id, x_center, y_center, width, height = map(float, values)

        # Convert YOLO coordinates to pixel values
        img_width, img_height = img.size
        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height

        # Calculate the bounding box coordinates
        x1 = int(x_center - width / 2)
        y1 = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)

        # Crop the image using the bounding box coordinates
        cropped_img = img.crop((x1, y1, x2, y2))

        # Save the cropped image
        cropped_img.save(f"{output_path}/{file_name}_crop_{i}.jpg")
        yield cropped_img


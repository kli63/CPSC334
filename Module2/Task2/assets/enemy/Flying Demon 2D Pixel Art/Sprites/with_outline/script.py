import os
import cv2
from pathlib import Path

# Create output directory for sprites
def create_output_directory(image_name):
    folder_name = image_name.lower().replace(' ', '_')  # lowercase the image name and replace spaces with underscores
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Function to split the image into sprites with each sprite being 81 pixels wide
def split_image_into_sprites(image_path, sprite_width=81):
    # Read the image with transparency (include alpha channel)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Error reading {image_path}")
        return

    # Check if the image has an alpha channel (transparency)
    if image.shape[2] != 4:
        print(f"Warning: {image_path} does not have an alpha channel, transparency may be lost.")
    
    # Get the height and width of the image
    image_height, image_width, _ = image.shape

    # Create output directory based on the image name
    image_name = Path(image_path).stem  # Get the image name without extension
    output_folder = create_output_directory(image_name)

    # Calculate the number of sprites based on the width
    num_sprites = image_width // sprite_width

    # Split the image into sprites of fixed 81-pixel width and save them
    sprite_count = 0
    for i in range(num_sprites):
        # Calculate the bounding box of the current sprite
        start_x = i * sprite_width
        end_x = start_x + sprite_width

        # Crop the sprite from the image (taking the full height of the image)
        sprite = image[:, start_x:end_x]

        # Save the sprite with transparency (PNG format)
        sprite_filename = os.path.join(output_folder, f'{sprite_count}.png')
        cv2.imwrite(sprite_filename, sprite, [cv2.IMWRITE_PNG_COMPRESSION, 9])  # PNG format to retain transparency
        sprite_count += 1

    print(f"Saved {sprite_count} sprites from {image_name} into folder {output_folder}")


# Main script to process all images in the folder
def process_images_in_directory():
    # Get the current directory
    current_directory = os.getcwd()

    # Iterate through all files in the directory
    for filename in os.listdir(current_directory):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(current_directory, filename)
            split_image_into_sprites(image_path)


if __name__ == "__main__":
    # Process all images in the current directory
    process_images_in_directory()
